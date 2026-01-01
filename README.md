```json
{
    "Z": {
        "type": "slot tag",
        "meaning": "현재 상황 / 현상"
    },
    "T": {
        "type": "slot tag",
        "meaning": "시간 / 흐름",
        "example": "T1400 -> 14시00분(절대 시간), Tp -> 과거, Tf -> 미래, Tn -> 현재, Tef -> 진행형, TdR3h -> 3시간 동안 지속, Tei -> 영구적 상태"
    },
    "K": {
        "type": "slot tag",
        "meaning": "원인 / 전제"
    },
    "F": {
        "type": "slot tag",
        "meaning": "결과 / 작용"
    },
    "N": {
        "type": "slot tag",
        "meaning": "생각 / 가치 판단"
    },
    "Im": {
        "type": "id tag",
        "meaning": "화자 (나)",
        "example": "ImAcamo -> 임아카모/내가 조작한다."
    },
    "Ym": {
        "type": "id tag",
        "meaning": "청자 (너)",
        "example": "YmAcamo -> 윰아카모/너가 조작한다."
    },
    "Om": {
        "type": "id tag",
        "meaning": "제3자/외부 객체",
        "example": "OmAcamo ->  씀아카모/누군가가 조작한다."
    },
    "Logic_Gates": {
        "-~ a'- ": {
            "meaning":"인과관계의 흐름 (A 때문에 B가 됨). / >",
            "example": "{ImAcavo} @Y eth {Lai~ a'Zaa}"
        },
        " aya ": "상호 영향 (A와 B가 서로 주고받음) / <>",
        "-~ sa'- ": {
            "meaning": "지연된 인과 (A가 시간이 흐른 뒤 B를 유발함) / ~>",
            "example": "{OmAcapoSu !~ sa'ImRaf}~ sa'[AcapoCu] eth F"
        },
        " | ": "a 혹은 b 중 하나. 예시: A|B. / A so B.에이 소 비",
        " en ": "동시 발생 (A와 B가 동시에 일어남). / =",
        " ! ": "즉각적인 대응이 필요한 데이터 (경고/위험).",
        " ? ": "데이터 확인 및 정보 탐색 요청 (질문).",
        " , ": "나열 및 병렬 처리",
        " Eth ": "데이터의 목적 및 성격 규정 (꼬리표). / ;",
        " no ": "부정 (Not/None) / ~",
        " R ": "A는 B이다. / :"
    },
    "Vector_Tags": {
        "Pu": "확장, 상승, 강화",
        "Mu": "축소, 하락, 약화",
        "Cu": "반전, 모순, 거부 (행동에서는 소극성) / Cu.큐",
        "Xu": "설명하기 힘든 모호한 상태 / Xu.쑤",
        "Su": "적극적, 물리적 강화 / Su.수",
        "Ju": "반복, 루프. /Jyu.쥬",
        "Hu": "효율적, 기계적 수행 / Hu.후"
    },
    "Number": {
        "example": "T1412 -> 트 외세외테 / Ra50Pu -> 라 네제푸",
        "0": "Ze",
        "1": "Oe",
        "2": "Te",
        "3": "Fe",
        "4": "Se",
        "5": "Ne",
        "6": "Ge",
        "7": "Le",
        "8": "Me",
        "9": "Ka"
    },
    "Vector_Suffix_Extension": {
        "[(1~5) × 10 + (1~5)]": {
            "setting": "지속성은 10의 자리(1: 10분 미만, 2: 30분 미만 및 10분 이상, 3: 1시간 미만 및 30분 이상, 4: 3시간 미만 및 1시간 이상  5: 3시간 이상), 변동성은 1의 자리(1: 안정적, 2: 불안한, 3: 불안정한, 4: 빠름, 5: 매우 빠름).",
            "example": "Ra50Pu -> 고강도 분노가 매우 오래 지속됨. (라네제푸)"
        },
        "@": "대상 지정 (Target) / tu.투"
    },
    "Scope_Tags": {
        "()": "내부, 본질, 비공개 데이터 (내면) / ( : nar.나르, ) : mr.므르",
        "[]": "외부, 표면, 공개 데이터 (행동) / [ : nor.노르, ] : nr.느르",
        "Md": "경계, 필터링 지점 / mor.모르",
        "{}": "논리적 그룹핑 / { : uir.의르, } : ur 우르"
    },
    "Certainy_Tags": {
        "ic": "확정된, 진리",
        "ec": "가변적인, 추측"
    },
    "Primary_Categories": {
        "Va": "결핍/필요 (Vab:육체, Vam:정신, Var:물리)",
        "La": "인지/지식 (Lam:기억, Lai:정보입력, Lac:추론, Lav:확인완료)",
        "Lia": "정보 및 데이터 (Liad : 수치 데이터, Liat: 텍스트/언어 정보, Liam: 미디어/시작 정보",
        "Ka": "충돌/대립, 오류",
        "Sa": "해소/획득 (Sab:육체, Sam:정신, Sar:물리)",
        "Dg": "위계/상급자",
        "Suba": "하위/객체",
        "Pa": "규칙/계약",
        "Za": "평온/수용 (Zas:휴식, Zaa(Zoe), Zaf:충족)",
        "Ra": "분노/거부 (Rai:짜증, Raf:공포, Ras:슬픔)",
        "Aca": {
            "meaning": "행위 / 행동",
            "derivation": {
                "Acapo": "물리적 행동 (Physical Action)",
                "Acavo": "언어적 발화 (Verbal Action)",
                "Acamo": "조작 및 제어 (Manipulation)"
            }
        },
        "Eg": {
            "meaning": "환경/객체",
            "derivation": {
                "Egoc": "위치/장소 / Egoc.에곡",
                "Egob": "사물/도구 / Egob.에곱",
                "Egev": "환경 조건(날씨, 온도, 조명 등) / Egev.에겝",
                "Exi": "시스템/프로세스 (기계적 절차) / Egsy.엑시"
            }
        },
        "Pin": {
            "meaning": "실행/계획",
            "derivation":{
                "Pinrdy": "준비/대기 / Pinrdi.핀르디",
                "Pinrun": "실행 중 / Pinrun.핀런",
                "Pinend": "완료/종료 / Pinend.피넨드",
                "Pinhold": "일시 중단/보류 / Pinhold. 핀홀드"
            }
        },
        "Val": "가치 존재",
        "Has": "소유/연결"
    },
    "fitr": {
        "#Burnout": "{Tef + KaRHigh + (RaPu)}",
        "#Flow": "{Tef + Lac + (ZafPu)}"
    },
    "Humanity_Tags": {
        "eta": "비논리적 직관",
        "ata": "공감/상태 공유",
        "uta": "상상/가능성"
    },
    "Examples": {
        "#Burnout~ a'[AcamoHu24] eth Z": "Burnout~ 아'노르 아캬모후테세 느르 에쓰 즈 / 번아웃 상태에서 기계적으로 1시간 이상 빠르게 업무를 조작 중인 현 상황.",
        "{OmAcapoSu !~ a'ImRaf}~ sa'[AcapoCu] eth F": "의르 옴아캬포수!~ 아'임라흐 우르~ 사'노르 아캬포큐 느르 에쓰 흐 / X의 공격적 행동(위험)이 공포를 유발하여 소극적 동작을 취하게 됨.",
        "{ImAcamo} @Exi eth Pinrun (Trf)~ a'{LiadPu}": "의르 임아캬모 우르 투 엑시 에쓰 핀런 나르 트르흐 므르~ 아'드르 리아드푸 / 나(I)는 시스템(Eg:sys)을 조작 중(mAg)이며, 현재 실행 중(Pg:run)인 프로세스를 통해 데이터(dIg)가 증가(+)하고 있음.",
        "[Egev(rain)] en {T1800}~ sa'[OmAcapoMu]": "노르 에겝 레인 느르 엔 드르 트외메제제 우르~ 사'노르 옴아캬포무 / 18시 정각(T:1800)에 비가 오기 시작함(Eg:env:rain). 이로 인해 외부 객체(X)들의 물리적 활동(pAg)이 감소(/)함.",
        "{YmAcavo} @I eth {Liat R ec}~ a'{ImLac~ a'NR?}": "의르 윰아캬보 우르 투 이 에쓰 드르 리아트 르 우크 우르~ 아'드르 임라크~ 아'느르? / 상대방(Y)이 나(I)에게 텍스트 정보(tIg)를 말했으나, 그것은 불확실(Uc)함. 이에 따라 나(I)는 추론(cLg) 후 판단을 보류/질문(N:?)함.",
        "{ImAcapo} @Egoc(Office) eth T0900 Ju {ImHas @Egob(Laptop)}": "의르 임아캬포 우르 투 에고크 오피스 에쓰 트제카제제 쥬 드르 임헤스 투 에곱 랍톱 / 09시 정각에 사무실(Office)로 이동함. 노트북(Laptop)을 소유(연결)한 상태임.",
        "ImnoHas": "임노헤스 / 내 것이 아니다."
    },
    "GlobalSettings": {
        "meaning": "전체적 설정. 언어의 규칙 정의.",
        "N1": {
            "setting": "Scope_Tags는 문장의 끝부분에서는 생략 가능.",
            "example": {"{ImAcavo} @Y eth {Lai~ a'Zaa}": "의르 임아카보 우르 투 유 에쓰 의르 라이~ 아'재 우르 -> 의르 임아카보 우르 투 유 에쓰 의르 라이~ 아'재"}
        },
        "N2": {
            "setting": "aa는 ae로 발음.",
            "example": {"Zaa": "Zae(=재)"}
        },
        "N3": {
            "setting": "C는 Ky로 발음.",
            "example": {"Acapo": "Acyapo(=아캬포)"}
        },
        "N4": {
            "setting": "J는 Jy로 발음.",
            "example": {"Ju": "Jyu(=쥬)"}
        }
    }
}
