import pandas as pd
import gensim
import streamlit as st
from streamlit_folium import folium_static
import folium

def main():
    df = pd.read_csv('data/final_data.csv')
    model_cbow = gensim.models.Word2Vec.load('data/final_model')

    st.title("제주픽")
    st.write("안녕하세요! 저희는 💫2달의사자🦁 입니다")
    st.write("아래 검색창에 키워드를 입력하시면 어울리는 제주도 식당을 추천해드립니다-!")
    st.write("\n")

    input_keyword = st.text_input(label="Search Keyword", value="")
    
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
                # main_keyword=keywords[0][0]
                flag = True
            except:
                con.error("죄송합니다. 유사한 키워드를 가지고 있는 식당이 없습니다. 다른 키워드를 입력해주세요!")
         
    if flag:

        weighted_series=pd.Series(df['Text_token']).apply(lambda x:1)

        for keyword, weight in keywords:
            count = pd.Series(df['Text_token'].apply(lambda x:x.count(keyword)))
            weighted_series += count*weight
        weighted_series = weighted_series.sort_values(ascending=False)

        index = weighted_series[weighted_series>0].index
        if len(index) > 5:
            index=index[:5]
        
        con.table(df['상호지점명'][index])
        # 검색 결과 df로 만들기
        recommend_restaurant = df['상호지점명'][index]
        rec_res=recommend_restaurant.to_frame()
        rec_res=rec_res.reset_index()
    
        # 지도 시각화를 위한 df 만들기
        del df['index']
        df = df.reset_index()
        matched_df = pd.merge(rec_res, df, left_on='index', right_on='index', how='inner')
        # 사용하지 않는 열 제거
        del matched_df['상호지점명_y']
        del matched_df['리뷰']
        del matched_df['Text']
        del matched_df['Text_token']
        matched_df.rename(columns={'상호지점명_x':'상호지점명'},inplace=True)

        # folium을 사용한 지도 시각화
        jeju_map = folium.Map(location=[33.4110625, 126.9367558], zoom_start=11)
        for item in range(len(matched_df)):
            lat = matched_df.loc[item, '위도']
            long = matched_df.loc[item, '경도']
            folium.Marker([lat,long], popup=matched_df.loc[item]['상호지점명'], icon=None).add_to(jeju_map)
        
        # streamlit에 불러오기
        folium_static(jeju_map)
        
if __name__ == '__main__' :
    main()
