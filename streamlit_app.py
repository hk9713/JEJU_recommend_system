import pandas as pd
import gensim
import streamlit as st


def main():
    df = pd.read_csv('data/result_jeju.csv')
    model_cbow = gensim.models.Word2Vec(sentences=df['review_token'], vector_size=100, window=3, min_count=0,workers=4,sg=0)

    st.title("제주도 맛집 추천 시스템")

    flag = True
    while flag:
        input_keyword = st.text_input(label="Search Keyword", value="키워드를 입력해주세요")
        if st.button("Search"):
            con = st.container()
            con.caption("Result")
            try:
                keywords=model_cbow.wv.most_similar(input_keyword)
                main_keyword=keywords[0][0]
                con.write(f"요청하신 키워드는 '{str(main_keyword)}' 입니다.")
                flag = False
            except:
                flag = True
                con.info("유사한 키워드를 가지고 있는 식당이 없습니다. 다른 키워드를 입력해주세요")

        count_series = pd.Series(df['review_token'].apply(lambda x:x.count(main_keyword)))
        count_series = count_series.sort_values(ascending=False)

        index = count_series[count_series>0].index
        if len(index) > 5:
            index=index[:5]

    con.table(df['상호명'][index])
    
if __name__ == '__main__' :
    main()