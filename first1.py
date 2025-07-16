import streamlit as st
import pandas as pd

st.set_page_config(page_title="2025년 5월 연령별 인구 현황", layout="wide")

st.title("2025년 5월 연령별 인구 현황 분석")
st.write("📂 업로드한 데이터를 기반으로 총인구수가 많은 상위 5개 행정구역의 연령별 인구 분포를 분석합니다.")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드해주세요 (EUC-KR 인코딩)", type="csv")

if uploaded_file:
    try:
        # CSV 파일 읽기
        df = pd.read_csv(uploaded_file, encoding='EUC-KR')
        
        # 연령별 컬럼만 추출
        age_cols = [col for col in df.columns if col.startswith("2025년05월_계_")]
        age_map = {col: col.replace("2025년05월_계_", "") for col in age_cols}
        df.rename(columns=age_map, inplace=True)

        # 나이 숫자만 있는 컬럼 리스트
        age_only_cols = list(age_map.values())

        # 총인구수가 있는지 확인
        if '총인구수' not in df.columns:
            df['총인구수'] = df[age_only_cols].sum(axis=1)

        # 상위 5개 행정구역 추출
        top5 = df.nlargest(5, '총인구수')

        # 📋 원본 데이터 출력
        st.subheader("📋 원본 데이터 (상위 20개 행만 표시)")
        st.dataframe(df.head(20))

        st.subheader("👑 총인구수 상위 5개 지역")
        st.dataframe(top5[['행정구역', '총인구수']])

        st.subheader("📈 상위 5개 지역의 연령별 인구 변화")

        # 그래프 출력
        for i, row in top5.iterrows():
            st.markdown(f"### 🏙️ {row['행정구역']}")
            data = pd.DataFrame({
                "연령": list(map(int, age_only_cols)),
                "인구수": row[age_only_cols].astype(int).values
            }).set_index("연령")
            st.line_chart(data)

    except Exception as e:
        st.error(f"❌ 오류가 발생했습니다: {e}")
else:
    st.info("📁 좌측에서 또는 위에서 파일을 업로드해주세요.")
