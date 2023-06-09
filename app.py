from fastapi import FastAPI
from PIL import Image

import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import advertools as adv
import main

def makeNavbar() :
  # Set page title
  st.set_page_config(page_title="Streamlit App")

  # Set logo and app name
  image = Image.open("logo.jpg")
  st.image(image, width=100)
  st.title("My Streamlit App")

  # Create navigation bar
  nav = st.container()

  with nav:
      st.markdown("""
          <style>
          .navbar-custom {
              color: black;
              background-color: #232429;
              padding: 20px 100px;
          }
          ul li {
            list-style: none;
          }
          ul li a {
            text-decoration: none;
          }
          </style>
          
          <nav class="navbar navbar-expand-lg navbar-custom">
            <div class="container-fluid">
              <a class="navbar-brand" href="#">Home</a>
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                  <li class="nav-item">
                    <a class="nav-link" href="#" >About</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link" href="#" >Contact</a>
                  </li>
                </ul>
              </div>
            </div>
          </nav>
      """, unsafe_allow_html=True)



num_messages = 0
words = 0

def sidebar():
  st.sidebar.title("Whatsapp Chat Analyzer")

  uploaded_file = st.sidebar.file_uploader("Choose a file")
  if uploaded_file is not None:
      bytes_data = uploaded_file.getvalue()
      data = bytes_data.decode("utf-8")
      df = preprocessor.preprocess(data)

      # fetch unique users
      user_list = df['user'].unique().tolist()
      # user_list.remove('group_notification')
      user_list.sort()
      user_list.insert(0,"Overall")

      selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

      if st.sidebar.button("Show Analysis"):

          # Stats Area
          num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)
          st.title("Top Statistics")
          col1, col2, col3, col4 = st.columns(4)

          with col1:
              st.header("Total Messages")
              st.title(num_messages)
          with col2:
              st.header("Total Words")
              st.title(words)
          with col3:
              st.header("Media Shared")
              st.title(num_media_messages)
          with col4:
              st.header("Links Shared")
              st.title(num_links)

          # monthly timeline
          st.title("Monthly Timeline")
          timeline = helper.monthly_timeline(selected_user,df)
          fig,ax = plt.subplots()
          ax.plot(timeline['time'], timeline['message'],color='green')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          # daily timeline
          st.title("Daily Timeline")
          daily_timeline = helper.daily_timeline(selected_user, df)
          fig, ax = plt.subplots()
          ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          # activity map
          st.title('Activity Map')
          col1,col2 = st.columns(2)

          with col1:
              st.header("Most busy day")
              busy_day = helper.week_activity_map(selected_user,df)
              fig,ax = plt.subplots()
              ax.bar(busy_day.index,busy_day.values,color='purple')
              plt.xticks(rotation='vertical')
              st.pyplot(fig)

          with col2:
              st.header("Most busy month")
              busy_month = helper.month_activity_map(selected_user, df)
              fig, ax = plt.subplots()
              ax.bar(busy_month.index, busy_month.values,color='orange')
              plt.xticks(rotation='vertical')
              st.pyplot(fig)

          st.title("Weekly Activity Map")

          # finding the busiest users in the group(Group level)
          if selected_user == 'Overall':
              st.title('Most Busy Users')
              x,new_df = helper.most_busy_users(df)
              fig, ax = plt.subplots()
          
              col1, col2 = st.columns(2)

              with col1:
                  ax.bar(x.index, x.values,color='red')
                  plt.xticks(rotation='vertical')
                  st.pyplot(fig)
              with col2:
                  st.dataframe(new_df)

          # WordCloud
          st.title("Wordcloud")
          df_wc = helper.create_wordcloud(selected_user,df)
          fig,ax = plt.subplots()
          ax.imshow(df_wc)
          st.pyplot(fig)

          # most common words
          most_common_df = helper.most_common_words(selected_user,df)

          fig,ax = plt.subplots()

          ax.barh(most_common_df[0],most_common_df[1])
          plt.xticks(rotation='vertical')

          st.title('Most commmon words')
          st.pyplot(fig)

          #emoji analysis
          emoji_df = helper.analyze_emojis(selected_user,df)
          
          st.title("Emoji Analysis")

          col1,col2= st.columns(2)

          with col1:
              st.dataframe(emoji_df)

print('Num messages',num_messages)
print('words',words)

# call the navbar
makeNavbar()
sidebar()

class stats:
    num_messages = int(num_messages)
    words = int(words)