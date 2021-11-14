import altair as alt
import pandas as pd
import streamlit as st
import os,time
os.environ['TZ'] = 'UTC'
time.tzset()
df=pd.read_csv("https://raw.githubusercontent.com/JennyliR/SI649data/main/Employment_Rank.csv")
yrs = [2000, 2005, 2010, 2015]
st.image('https://raw.githubusercontent.com/JennyliR/SI649data/main/redlake_title.jpg')

year_select = st.selectbox(label='In Year',
                             options=yrs, index=3)
st.title('Red Lake County Ranks')

#Chart1
##Category Selection
selection = alt.selection_single() #1
opacity = alt.condition(selection, alt.value(1), alt.value(0.5))
##Category Selection
selection = alt.selection_single(nearest=True, encodings=['y'], init={'y':'Income Per Capita'}) #selection for category
opacity = alt.condition(selection, alt.value(1), alt.value(0.5))
##Bar Chart
bar = alt.Chart(df, width=700, height=200).mark_bar(size=50).encode(
  alt.X('Rank:Q',title = None,axis=None),
  alt.Y('Category',title = None, axis=None,sort=alt.EncodingSortField(
        field='Rank', order='ascending'
    )), tooltip=['Category', 'Value', 'Unit'],
    color = alt.Color("Category:N", legend=None),
    opacity = opacity
).transform_filter(
    (alt.datum.Location == "Red Lake, MN") & (alt.datum.Year == int(year_select))   #Dropdown
)

##Bar Chart Text
text1 = bar.mark_text(size = 25, dx = 10, align='left').encode(
    alt.Y('Category',sort=alt.EncodingSortField(
        field='Rank', order='ascending'
    )),
    text= alt.Text('label:O')
).transform_calculate(label='"#" + datum.Rank + " in " + datum.Category')

##line charts
highlight = alt.selection(type='single', on='mouseover',
                          fields=['Location'], nearest=False, empty='none')
selection2 = alt.selection_interval(bind='scales', encodings=['y'])

points = alt.Chart(df, width=500, height=150).mark_circle().encode(
    alt.X('Year:O',title = None),
    alt.Y('Value:Q',title = None, axis=None),
    opacity=alt.value(0),
    #size = alt.value(10),
    color = alt.condition(alt.datum.Location == 'Red Lake, MN', 'Location:N', alt.value("#997F6A"), legend=None),
    tooltip=['Location','Value', 'Unit', 'Year'],
).transform_filter(
    selection).transform_filter(alt.datum.Location != 'Minnesota').properties(width=600 height= 400) #Changed

line = alt.Chart(df, width=500, height=150).mark_line(size=1, color='darkred').encode(
    alt.X('Year:O',title = None),
    alt.Y('Value:Q',title = None, axis=None,),
    tooltip=['Location','Value', 'Unit', 'Year'],
    size=alt.value(3)
).transform_filter(
    selection).transform_filter(alt.datum.Location == 'Red Lake, MN').transform_filter(alt.datum.Location != 'Minnesota').properties(width=600, height= 200)


line2 = alt.Chart(df, width=500, height=150).mark_line(size=1).encode(
    alt.X('Year:O',title = None, axis=None),
    alt.Y('Value:Q',title = None, axis=None),
    tooltip=['Location','Value', 'Unit', 'Year'],
    color = alt.condition(alt.datum.Location == 'Red Lake', 'Location:N', alt.value("#997F6A"), legend=None),
    opacity = alt.condition(highlight, alt.value(1), alt.value(0.8)),
    
    size=alt.condition(highlight, alt.value(5), alt.value(1))
).transform_filter(selection # & (alt.datum.Location != 'Red Lake, MN')
                  ).transform_filter(alt.datum.Location != 'Minnesota').properties(width=600, height= 200)


text2 = line.mark_text(size = 30, dx = 10, align='left').encode(
    alt.X('Year:O',title = None),
    alt.Y('Value:Q',title = None, axis=None),
    tooltip=['Location','Value', 'Unit', 'Year'],
    text = alt.Text('Location'),
    size = alt.value(20),
    color = alt.value('darkred')
).transform_filter(
    selection).transform_filter((alt.datum.Location == 'Red Lake, MN')
    & (alt.datum.Year == 2015)).properties(width=600, height= 200)

rule=alt.Chart(df).mark_rule(color='#F0B863',size=25, strokeOpacity=0.1, fillOpacity=0.1, opacity=0.1).encode(
    alt.X('Year:T'),
).transform_filter(alt.datum.Year == int(year_select))

line_axis = alt.Chart(df, width=900).mark_text(size = 10, dy = 100, align='center', color='#996C46').encode(
    alt.X('Year:T',title = None),
    text= alt.Text('Year:O')
).transform_filter(alt.datum.Location == 'Red Lake, MN')

line_title = alt.Chart(df, width=900).mark_text(size = 15, dy = -120, align='center', color='#996C46').encode(
    text= alt.Text('label2:O')
).transform_filter((alt.datum.Year == int(year_select))& alt.datum.Location == 'Red Lake, MN').transform_filter(selection
).transform_calculate(label2='"Minnesota State "+ datum.Category + " from 2000 to 2015"')

#Second Bar Chart
bar2 = alt.Chart(df, width=200, height=150).mark_bar(size=20).encode(
  alt.X('Location:N',title = None,sort=alt.EncodingSortField(
        field='Value', order='ascending'
    ), axis=None),
  alt.Y('Value:Q',title = None, axis=None),
    color = alt.condition(alt.datum.Location == 'Red Lake, MN', alt.value('darkred'), 
                          alt.value("#997F6A"), legend=None),
    tooltip=['Location','Value', 'Unit', 'Year'],
).transform_filter(
    ((alt.datum.Location == "Red Lake, MN"
     ) | (alt.datum.Location == "Minnesota"
     ) |(alt.datum.Rank == 1)|(alt.datum.Rank == 87)
    ) & (alt.datum.Year == int(year_select)) #Dropdown
).transform_filter(selection).properties(title='Red Lake Compared with Max, Min and State Average')

bar_text = bar2.mark_text(size = 15, dy = -15, align='center').encode(
    alt.X('Location:N',title = None,sort=alt.EncodingSortField(
        field='Value', order='ascending'
    )
         ),
    text= alt.Text('Location:N')
)


vis1= ((bar.add_selection(selection)+text1)&(
 (line2.add_selection(highlight, selection2)+rule+line+text2+points+line_axis+line_title)|(bar2+bar_text))).configure_view(strokeWidth=0).resolve_scale(color='independent', size='independent'
 ).configure_range(category={'scheme': 'browns'}).configure_title(
    color='#996C46',
    fontSize=16
)


##Display

st.altair_chart(vis1, use_container_width=False)
st.markdown('2015 is a great year for Red Lake County Residents, while their **_Population_** slightly dropped like the most counties in the state, their **_Personal Income Per Capita_** increased drastically. In fact, compared to 2000, their income per capita increased **101.47%**.')
st.markdown('**_Farm Income Total_** had experience drop from 2000 to 2005, but in 2015 the farm income bounced back to 21653 thousands of dollar, higher than 2000\'s farm income total.')
