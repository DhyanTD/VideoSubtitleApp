<template>
  <div>
   
    <div class="video-list">
      <div
        v-for="video in videos"
        :key="video.name"
        class="video-thumbnail"
        @click="playVideo(video)"
      >
        <img :src="getThumbnailUrl(video.thumbnail)" alt="Video Thumbnail" />
        <span>{{ video.name }}</span>
      </div>
    </div>
   

    <div v-if="selectedVideo" class="video-player">
      <video controls :src="getVideoUrl(selectedVideo.name)" @timeupdate="updateSubtitles"></video>
      <div v-if="subtitles && currentSubtitleIndex >= 0 && currentSubtitleIndex < subtitles.length" class="subtitles" style="color:black;">
        {{ subtitles[currentSubtitleIndex].text }}
      </div>
    </div>
    
  </div>
</template>

<script>

import axios from 'axios';

export default {
  data() {
    return {
      videos: [],
      selectedVideo: null,
      subtitles: [],
      currentSubtitleIndex: -1
    };
  },
  methods: {
    async fetchVideos() {
      try {
        const response = await axios.get('http://159.65.153.73:5000/get_uploaded_videos');
        this.videos = response.data.videos;
      } catch (error) {
        console.error(error);
      }
    },
    getThumbnailUrl(thumbnail) {
      return thumbnail
        ? `http://159.65.153.73:5000/thumbnails/${thumbnail}`
        : require('@/assets/default-thumbnail.jpg'); // Path to default thumbnail
    },
    getVideoUrl(videoName) {
      return `http://159.65.153.73:5000/videos/${videoName}`;
    },
    playVideo(video) {
      this.selectedVideo = video;
    },
   async fetchSubtitles(videoName) {
      try {
        const response = await axios.get(`http://159.65.153.73:5000/get_subtitles/${videoName}`);
        this.subtitles = response.data.subtitles;
        // console.log('Subtitles:', this.subtitles);
      } catch (error) {
        console.error(error);
      }
    },
    updateSubtitles(event) {
      const videoElement = event.target;
      const currentTime = videoElement.currentTime;
      const formattedCurrentTime = this.formatTime(currentTime);
      
      // console.log(formattedCurrentTime);
      for (let i = 0; i < this.subtitles.length; i++) {
        const subtitle = this.subtitles[i];
        // console.log("jhgg",subtitle.startTime);
        if (formattedCurrentTime >= subtitle.startTime && formattedCurrentTime < subtitle.endTime) {
          this.currentSubtitleIndex = i;
          return;
        }
      }
      
      this.currentSubtitleIndex = -1;
    },
    formatTime(time) {
      const hours = Math.floor(time / 3600);
      const minutes = Math.floor((time % 3600) / 60);
      const seconds = (time % 60).toFixed(3);
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.padStart(6, '0')}`;
    },
  },
  mounted() {
    this.fetchVideos();
  },
   watch: {
    selectedVideo(newVideo) {
      this.fetchSubtitles(newVideo.name);
    },
  },
};
</script>

<style>

.upload-form {
  margin-bottom: 20px;
}

.video-list {
  display: flex;
  flex-wrap: wrap;
}

.video-thumbnail {
  margin: 10px;
  cursor: pointer;
}

.video-thumbnail img {
  width: 200px;
  height: 150px;
}

.video-player {
  margin-top: 20px;
}
.subtitles{
  color:black
}
</style>
