import pandas as pd
import pickle
import streamlit as st

def main():
    df = pd.read_csv('data/final.csv')
    with open('cbow_model.pickle','rb') as f:
        model_cbow = pickle.load(f)

    st.title("키워드를 통한 제주도 맛집 추천 시스템")

    input_keyword = st.text_input(label="Search Keyword", value="키워드를 입력해주세요")
    
    flag = False
  
    if st.button("Search"):
        con = st.container()
        con.caption("Result")
        
        if len(input_keyword) == 0:
            con.warning("키워드를 입력해주세요")
        else:
            try:
                con.write(f"요청하신 키워드는 '{str(input_keyword)}' 입니다.")
                keywords=model_cbow.wv.most_similar(input_keyword)
                main_keyword=keywords[0][0]
                flag = True
            except:
                con.info("유사한 키워드를 가지고 있는 식당이 없습니다. 다른 키워드를 입력해주세요")
                flag = False
         
    if flag:
        weighted_series=pd.Series(df['token'].apply(lambda x:1))
        for keyword, weight in keywords:
            count = pd.Series(df['token'].apply(lambda x:x.count(keyword)))
            weighted_series += count*weight
        weighted_series = weighted_series.sort_values(ascending=False)

        index = weighted_series[weighted_series>0].index
        if len(index) > 5:
            index=index[:5]

        con.table(df['상호명'][index])
        
        
if __name__ == '__main__' :
    main()
