import os, requests, math
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Model
import sentencepiece as spm
from tensorflow.keras import mixed_precision

# =========================
# 설정
# =========================
TOKENIZER_PATH = "bpe.model"
DATA_PATH = "shuffled_corpus.txt"
MAX_LEN = 384
EMBED_DIM = 512
LATENT_DIM = 512
BATCH_SIZE = 768 
EPOCHS = 1
SHUFFLE_BUFFER = 200000
LEARNING_RATE = 1e-4
DROPOUT_AUG = 0.1
EMBED_DROPOUT = 0.1
SEED = 42

tf.get_logger().setLevel("ERROR")
tf.random.set_seed(SEED)
np.random.seed(SEED)

# =========================
# TPU 초기화
# =========================
on_tpu = False
try:
    resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu="local")
    tf.tpu.experimental.initialize_tpu_system(resolver)
    strategy = tf.distribute.TPUStrategy(resolver)
    print("✅ TPU 초기화 완료")
    on_tpu = True
except Exception as e:
    print("⚠️ TPU 미사용, GPU/CPU 진행")
    strategy = tf.distribute.get_strategy()

policy = mixed_precision.Policy("mixed_bfloat16" if on_tpu else "float32")
mixed_precision.set_global_policy(policy)

# =========================
# Tokenizer & Data Pipeline
# =========================
sp = spm.SentencePieceProcessor()
if os.path.exists(TOKENIZER_PATH):
    sp.load(TOKENIZER_PATH)
    pad_id = sp.piece_to_id("<pad>")
    if pad_id == -1: pad_id = 0
    vocab_size = sp.get_piece_size()
else:
    vocab_size = 8000 # Dummy for structure
    pad_id = 0

def encode_sentence_py(s: str):
    ids = sp.encode(s, out_type=int)[:MAX_LEN]
    ids = ids + [pad_id] * (MAX_LEN - len(ids))
    return np.array(ids, dtype=np.int32)

def tf_encode(line):
    def _encode_py(s_tensor):
        s = s_tensor.numpy().decode("utf-8")
        return encode_sentence_py(s)
    ids = tf.py_function(func=_encode_py, inp=[line], Tout=tf.int32)
    ids.set_shape([MAX_LEN])
    return ids

def token_dropout(tokens, drop_prob=DROPOUT_AUG):
    rnd = tf.random.uniform(tf.shape(tokens), 0, 1)
    keep_mask = rnd > drop_prob
    return tf.where(keep_mask, tokens, tf.cast(pad_id, tf.int32))

ds = tf.data.TextLineDataset(DATA_PATH)
ds = ds.map(lambda x: tf.strings.strip(x), num_parallel_calls=tf.data.AUTOTUNE).filter(lambda x: tf.not_equal(x, ""))
ds = ds.map(tf_encode, num_parallel_calls=tf.data.AUTOTUNE)
ds = ds.shuffle(SHUFFLE_BUFFER, seed=SEED).repeat()
ds = ds.map(lambda t: (token_dropout(t), token_dropout(t)), num_parallel_calls=tf.data.AUTOTUNE)
ds = ds.batch(BATCH_SIZE, drop_remainder=True)
ds = ds.map(lambda v1, v2: ((v1, v2), tf.zeros([BATCH_SIZE])), num_parallel_calls=tf.data.AUTOTUNE)
ds = ds.prefetch(tf.data.AUTOTUNE)

# =========================
# Model Layers
# =========================
class L2NormLayer(layers.Layer):
    def call(self, inputs):
        return tf.math.l2_normalize(inputs, axis=1)

class SentenceEncoder(Model):
    def __init__(self, vocab_size, embed_dim=EMBED_DIM, latent_dim=LATENT_DIM, max_len=MAX_LEN, pad_id=pad_id):
        super().__init__()
        self.pad_id = pad_id
        self.embed = layers.Embedding(vocab_size, embed_dim)
        self.pos_embed = layers.Embedding(input_dim=max_len, output_dim=embed_dim)
        self.dropout = layers.Dropout(EMBED_DROPOUT)
        self.attn = layers.Attention()
        self.WB1 = layers.Dense(2048, activation='gelu') # SimSiam은 MLP가 중요함
        self.bn1 = layers.BatchNormalization()
        self.WB2 = layers.Dense(latent_dim)
        self.bn2 = layers.BatchNormalization()
        self.attn_pool = layers.Dense(1)
        self.ln_f = layers.LayerNormalization(epsilon=1e-5)

    def call(self, x, training=None):
        positions = tf.range(tf.shape(x)[1])[tf.newaxis, :]
        x_embed = self.embed(x) + self.pos_embed(positions)
        x_embed = self.dropout(x_embed, training=training)

        mask = tf.cast(tf.not_equal(x, self.pad_id), tf.float32)
        h = self.attn([x_embed, x_embed])
        h = self.WB1(h)
        h = self.bn1(h, training=training)
        h = self.WB2(h)
        h = self.bn2(h, training=training)
        h = self.ln_f(h)

        scores = tf.cast(self.attn_pool(h), tf.float32)
        scores = tf.where(mask[..., tf.newaxis] == 0, -1e9, scores)
        scores = tf.nn.softmax(scores, axis=1)

        pooled = tf.reduce_sum(h * scores, axis=1)
        return tf.cast(pooled, tf.float32)

class Predictor(layers.Layer):
    def __init__(self, latent_dim=LATENT_DIM):
        super().__init__()
        # Bottleneck 구조 (SimSiam 논문: latent/4)
        self.fc1 = layers.Dense(latent_dim // 4, use_bias=False)
        self.bn = layers.BatchNormalization()
        self.fc2 = layers.Dense(latent_dim)

    def call(self, x, training=None):
        x = self.fc1(x)
        x = self.bn(x, training=training)
        x = tf.nn.relu(x)
        x = self.fc2(x)
        return x

# =========================
# SimSiam Wrapper & Loss
# =========================
def build_simsiam_model(vocab_size):
    encoder = SentenceEncoder(vocab_size)
    predictor = Predictor()
    
    input1 = layers.Input(shape=(MAX_LEN,), dtype=tf.int32)
    input2 = layers.Input(shape=(MAX_LEN,), dtype=tf.int32)
    
    z1 = encoder(input1)
    z2 = encoder(input2)
    
    p1 = predictor(z1)
    p2 = predictor(z2)
    
    # 학습 시 loss 계산을 위해 stack하여 출력
    out = tf.stack([p1, p2, z1, z2], axis=1) 
    return Model(inputs=[input1, input2], outputs=out), encoder

def simsiam_loss(y_true, y_pred):
    p1, p2, z1, z2 = y_pred[:,0], y_pred[:,1], y_pred[:,2], y_pred[:,3]

    def D(p, z):
        # Stop-gradient: SimSiam의 핵심 (Collapse 방지)
        z = tf.stop_gradient(z)
        p = tf.math.l2_normalize(p, axis=1)
        z = tf.math.l2_normalize(z, axis=1)
        return -tf.reduce_mean(tf.reduce_sum(p * z, axis=1))

    return (D(p1, z2) + D(p2, z1)) * 0.5

# =========================
# Training
# =========================
with strategy.scope():
    model, encoder = build_simsiam_model(vocab_size)
    optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
    model.compile(optimizer=optimizer, loss=simsiam_loss)

steps_per_epoch = 1000 # 데이터량에 따라 조정
model.fit(ds, epochs=EPOCHS, steps_per_epoch=steps_per_epoch)

encoder.save_weights("simsiam_encoder.weights.h5")
print("✅ SimSiam 학습 완료 및 가중치 저장")
