from konlpy.tag import Okt
import pandas as pd
import gensim
import streamlit as st

# preparing dataset
def setting_data():
    df = pd.read_csv('data/kakao_jeju_final.csv')
    
    # 데이터 전처리
    del df['Unnamed: 0']  
    df['kakao_blog_review_txt'] = df['kakao_blog_review_txt'].fillna('')
    
    return df

# okt tokenizer
def kakao_tokenizing(row):
    okt = Okt()
    row = okt.normalize(row)
    row = row.replace("#","").replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

    raw_pos_tagged = okt.pos(row, norm=True, stem=True)
    del_list = ['제주','제주도','특별자치도','서귀포시','제주시','성산','성산읍',
                '어제','오늘','우리','이틀','금요일','도착','출발',
                '하다', '있다', '되다', '이다', '돼다', '않다', '그렇다', '아니다', '이렇다', '그렇다', '어떻다','계시다'] 

    word_cleaned = []
    for word in raw_pos_tagged:
        if word[1] in ["Noun", "Adjective"]:
            if (len(word[0]) != 1) & (word[0] not in del_list):
                word_cleaned.append(word[0])
    # print(word_cleaned)
    return word_cleaned

# creating cbow model
def cbow_modeling(df):
    df['review_token'] = df['kakao_blog_review_txt'].apply(kakao_tokenizing)
    model_cbow = gensim.models.Word2Vec(sentences=df['review_token'], vector_size=100, window=3, min_count=0,workers=4,sg=0)
    return df, model_cbow

# recommend system
def recommend_system(df, model_cbow):
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
        
        return con.write(df['상호명'][index])

# streamlit
def main():
    st.title("제주도 맛집 추천 시스템")

    df = setting_data()
    df, model = cbow_modeling(df)
    recommend_system(model)
    
if __name__ == '__main__' :
    main()