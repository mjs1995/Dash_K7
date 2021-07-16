import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely import wkt
import pydeck as pdk
from scipy import stats
from scipy.stats import norm
import seaborn as sns
import matplotlib.pyplot as plt

#########################################################################################
### page 설정
st.sidebar.title('K7 상권분석')
option=st.sidebar.selectbox('k7매출을 활용한 데이터분석',('데이터EDA','결과'))

#########################################################################################
### data table
if option=='데이터EDA':
    st.title('K7 매출데이터를 활용한 상권분석')
    @st.cache(allow_output_mutation=True)

    def obj_to_geo(data):
        data['geometry'] = data['geometry'].apply(wkt.loads)
        return gpd.GeoDataFrame(data)
    path = 'https://raw.githubusercontent.com/mjs1995/Visualization/main/dash_app/data/%EC%84%9C%EC%9A%B8_merged.csv'
    df = pd.read_csv(path,encoding='cp949')

    st.subheader( "K7 매출 데이터")
    st.write(df[['region3','sale_dy','store_cd','item_class_cd','sale_amt_x','sale_qty','sale_amt_y']])
#########################################################################################
### geocoding
    df1 = pd.read_csv('https://raw.githubusercontent.com/mjs1995/Visualization/main/dash_app/data/%EC%84%9C%EC%9A%B8_merged.csv',encoding='cp949')
    from shapely import wkt
    df1['geometry'] = df1['geometry'].apply(wkt.loads)
    df1 = gpd.GeoDataFrame(df1)
    def polygon_to_coordinates(x):
        lon, lat = x.exterior.xy
        return [[x, y] for x, y in zip(lon, lat)]
    def multipolygon_to_coordinates(x):
        lon, lat = x[0].exterior.xy
        return [[x, y] for x, y in zip(lon, lat)]
    data = gpd.read_file('https://raw.githubusercontent.com/mjs1995/Visualization/main/dash_app/data/%EC%84%9C%EC%9A%B8%EB%B2%95%EC%A0%95%EB%8F%99.geojson')
    data['coordinates'] = data['geometry'].apply(multipolygon_to_coordinates)
    del data['geometry']
    data = pd.DataFrame(data)
    df1['coordinates'] = df1['geometry'].apply(multipolygon_to_coordinates)
    del df1['geometry']
    df = pd.DataFrame(df1)
    MAPBOX_API_KEY = "pk.eyJ1IjoibWpzMTk5NSIsImEiOiJja2pyM3AyZjEwMzZ6MnltdTA4aDc1NjJkIn0.SN28pnAUfydkAeMtp28uMw"
    df['정규화인구'] = df['sale_amt_x'] / df['sale_amt_x'].max()
    data = gpd.read_file('https://raw.githubusercontent.com/mjs1995/Visualization/main/dash_app/data/%EC%84%9C%EC%9A%B8%EB%B2%95%EC%A0%95%EB%8F%99.geojson')
    data['coordinates'] = data['geometry'].apply(multipolygon_to_coordinates)
    del data['geometry']
    data = pd.DataFrame(data)

    df_TB = gpd.read_file('https://raw.githubusercontent.com/mjs1995/Visualization/main/dash_app/data/TBGIS.geojson')
    df_TB['coordinates'] = df_TB['geometry'].apply(polygon_to_coordinates)
    del df_TB['geometry']
    df_TB = pd.DataFrame(df_TB)
############################################################################################
### distplot
    st.subheader('매출액 Distribution')
    f, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.distplot(df['sale_amt_x'], fit = norm, ax=axes[0])
    stats.probplot(df['sale_amt_x'], plot = axes[1])[1]
    st.pyplot(f)

############################################################################################
### heatmap
    st.subheader('매출액 Heatmap')
    cor = df[['sale_dy','store_cd','item_class_cd','sale_amt_x','sale_qty']].corr()
    fig = plt.figure(figsize = (15,10))
    sns.heatmap(cor, annot=True, cmap = "BuGn")
    st.pyplot(fig)

############################################################################################
### SELECTBOX widgets
    metrics =['발달상권','골목상권']
    st.title('상권종류별 영역')
    cols = st.selectbox('상권 종류', metrics)

# let's ask the user which column should be used as Index
    if cols in metrics:
        metric_to_show = cols
    df_bal = df_TB[df_TB['TRDAR_SE_1'] == metric_to_show].reset_index()

########################################################################################
## MAP
# Set viewport for the deckgl map
    st.title('K7 주위 상권 시각화')
    layer_poly = pdk.Layer(
    'PolygonLayer',
    data,
    get_polygon = 'coordinates',
    get_fill_color = '[0,0,0,50]',
    pickable = True,
    auto_highlight = True
    )

    layer = pdk.Layer(
        'PolygonLayer',
        df,
        get_polygon='coordinates',
        get_fill_color='[257, 250*정규화인구,255 ,1000*정규화인구]',
        pickable=True,
        auto_highlight=True
    )

    layer_M = pdk.Layer(
    'ScatterplotLayer',
    df,
    get_position='[x, y]',
    get_radius = 90,
    get_fill_color = '[255,0,0]',
    pickable = True,
    auto_highlight = True
    )

    layer_bal = pdk.Layer(
        'PolygonLayer',
        df_bal,
        get_polygon='coordinates',
        get_fill_color='[0, 255, 0, 150]',#'[64, 255,0]',
        pickable=True,
        auto_highlight=True
    )

    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10)

    r = pdk.Deck(layers=[layer_poly,layer,layer_M,layer_bal],
                map_style='mapbox://styles/mapbox/outdoors-v11',
                mapbox_key=MAPBOX_API_KEY,
                initial_view_state=view_state,
                tooltip={"html": "<b>주소:</b> {region3}"
                     "<br/> <b>매출액:</b> {sale_amt_y}"})
    st.pydeck_chart(r)

#########################################################################################
### Draw sidebar
if option=='결과':
    st.title('버전 업데이트 준비중입니다! 👋')
