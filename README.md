# Brand Design Skill

브랜드 철학과 기하학 규칙을 입력받아 벡터 로고를 설계·변주하는 범용 Codex 스킬입니다. **Reprism은 `examples/reprism/`의 디자인 예시**로 분리했습니다. 공통 스킬에는 R, 민트 색상, 특정 폰트·그리드·각도를 기본값으로 넣지 않습니다.

- [범용 스킬](brand-design/SKILL.md): 철학 → 도형 연산 → 변수 → 시각 효과 → 검증
- [입력 형식](brand-design/references/brief-contract.md): 자연어 요청을 구조화하는 기준
- [기하학 설계 원칙](brand-design/references/geometric-construction.md): Google·Pentagram·IBM의 원문 사례
- [생성 레시피](brand-design/references/recipe-contract.md): 변수·수식·도형·변환·팔레트·의미 연결
- [Reprism 사례](examples/reprism/case-study.md): 입력, 레시피, 라이선스, 기존 시안과 구현 한계

## 사용

`brand-design` 폴더 전체를 Codex의 사용자 스킬 디렉터리에 설치한 후 `$brand-design`로 사용합니다. 예시 폴더나 Reprism 웹 프로젝트가 없어도 사용할 수 있습니다. 별도 브랜드별 스킬을 만들지 않고, 새 브리프와 레시피로 변주합니다.

예를 들어:

> $brand-design 브랜드명은 …, 철학은 탐구·점진적인 발견·차분함. 규칙은 공통 그리드와 의미 있는 여백을 사용할 것. 책·전구 아이콘은 피하고 32px 웹 헤더에서 쓸 로고를 개방적인 형태와 압축적인 형태로 변주해줘.

사용자는 자연어로 입력해도 됩니다. 스킬이 설계 결정을 정리하고, 도형 생성 도구가 명시된 레시피를 실행합니다. 도구가 의미나 미적 품질을 자동 판정하는 것은 아닙니다.

범용 심볼 생성기는 Python 3.10+ 표준 라이브러리만 사용합니다. 폰트 설치나 네트워크 요청 없이 실행됩니다:

```sh
python brand-design/scripts/render_geometry.py \
  --brief examples/reprism/brief.json \
  --recipe examples/reprism/recipe.json \
  --output /your/output/directory
```

같은 변수로 심볼·구성도·해석된 변수 및 철학 연결 기록을 생성합니다. 워드마크의 폰트 선택·경로화는 별도 제작 단계입니다. 예시에 보존된 기존 워드마크 제작 도구만 FontTools 4.65.0과 Manrope를 사용하며, [폰트 라이선스](examples/reprism/assets/fonts/OFL.txt)를 함께 보존합니다.

## Reprism 디자인 예시

6단위 그리드·일정 두께·원호·45° 대각선을 사용한 기하학적 R의 기준 시안입니다. 이후 논의한 여러 관점의 투영 철학은 아직 구현되지 않았으므로 레시피와 생성 기록에 미완료로 표시합니다. 이 시안의 수치를 다른 브랜드에 강제하지 않습니다.

![Reprism 기하학적 R 시안](examples/reprism/preview.png)
