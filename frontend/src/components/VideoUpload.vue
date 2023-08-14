<template>
  <div>
    <h1>Video Upload App</h1>
    <input type="file" ref="fileInput" @change="handleVideoChange" accept="video/*">
    <input type="file" ref="thumbnailInput" @change="handleThumbnailChange">
    <button @click="uploadVideo">Upload Video</button>

   <div>
      <input type="text" v-model="subtitleText" placeholder="Enter subtitle text">
      <input type="time" v-model="subtitleStartTime" step="1">
      <input type="time" v-model="subtitleEndTime" step="1">
      <button @click="addSubtitle">Add Subtitle</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      uploadedVideos: [],
      selectedVideoFile: null,
      selectedThumbnailFile: null,
      subtitleText: '',
      subtitleStartTime: '00:00:00.000',
      subtitleEndTime: '00:00:00.000',
    };
  },
  methods: {
    async fetchVideos() {
      try {
        const response = await axios.get('http://localhost:5000/get_uploaded_videos');
        this.uploadedVideos = response.data.videos;
      } catch (error) {
        console.error(error);
      }
    },
    handleVideoChange(event) {
      this.selectedVideoFile = event.target.files[0];
    },
    handleThumbnailChange(event) {
      this.selectedThumbnailFile = event.target.files[0];
    },
    async uploadVideo() {
      if (!this.selectedVideoFile || !this.selectedThumbnailFile) {
        alert('Please select both video and thumbnail files.');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.selectedVideoFile);
      formData.append('thumbnail', this.selectedThumbnailFile);

      try {
        await axios.post('http://localhost:5000/upload', formData);
        this.fetchVideos();
        alert('Files uploaded successfully');
      } catch (error) {
        console.error(error);
        alert('Error uploading files');
      }
    },
   
    getVideoUrl(videoName) {
      return `http://localhost:5000/videos/${videoName}`;
    },
    async addSubtitle() {
      if (!this.selectedVideoFile) {
        alert('Please select a video.');
        return;
      }

      try {
        await axios.post('http://localhost:5000/add_subtitle', {
          videoName: this.selectedVideoFile.name,
          text: this.subtitleText,
          startTime: this.subtitleStartTime,
          endTime: this.subtitleEndTime,
        });

        this.subtitleText = '';
        this.subtitleStartTime = '00:00:00.000';
        this.subtitleEndTime = '00:00:00.000';

        alert('Subtitle added successfully');
      } catch (error) {
        console.error(error);
        alert('Error adding subtitle');
      }
    },
  },
  
  mounted() {
    this.fetchVideos();
  },
};
</script>
