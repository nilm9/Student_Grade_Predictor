<template>
  <div>
    <!-- Application Header -->
    <header   >
      <h2 class="subtitle" >GradeGenius.ai</h2>

          <h1 class="title">Your Pathway to Academic Insight</h1>
      <!-- Application Header <img src="../../public/header.png" alt="header book neon" style="width:20rem;"> -->
      <div class="hero-header">
                  <Button label="Get Started"  />
          <Button label="Sing in"  />
      </div>

    </header>


    <!-- Main Content Area -->
    <div class="content">

          <div style="margin:5rem 0rem;">

          <h2>Welcome to GradeGenius</h2>

          <p>Welcome to GradeGenius, a user-friendly tool designed to help students and educators unlock the power of data in academics. Explore predictive analytics to enhance understanding of student performance, tailor educational strategies, and support academic success...</p>
          </div>

  <div class="grid-stack">



      <Card>
        <template #title>
          <h2>Unveal Trends</h2>
        </template>
        <template #content>
          <p>Discover how GradeGenius’s predictive analytics can enhance your understanding of student performance, tailor educational strategies, and support academic success...</p>
<i class="pi pi-book" style="font-size: 3rem; color:var(--primary-color);"></i>

        </template>
      </Card>

      <Card >
        <template #title>
          <h2>Interactive Visualization</h2>
        </template>
        <template #content>
          <p>Engage with our intuitive data visualizations in GradeGenius to uncover trends in student grades, attendance, and other key performance indicators...</p>
<i class="pi pi-chart-line " style="font-size: 3rem; color:var(--primary-color);"></i>

        </template>
      </Card>

      <Card>
        <template #title>
          <h2>Compute in the cloud</h2>

        </template>
        <template #content>
          <p>Begin your journey towards data-driven educational insights. Upload your school's database to predict grades and access personalized insights with GradeGenius...</p>
<i class="pi pi-cloud-upload" style="font-size: 3rem; color:var(--primary-color);"></i>

        </template>
      </Card>
 </div>
        <div style="margin:5rem 0rem;">
          <h2>Get Started with GradeGenius</h2>


          <p>Begin your journey towards data-driven educational insights. Upload your school's database to predict grades and access personalized insights with GradeGenius...</p>
          <div class="hero-header">

                      <Button label="Upload Database" icon="pi pi-upload" />
          <Button label="Predict Grades" icon="pi pi-chart-line" />
          </div>


</div>
    </div>
  </div>
</template>






<script setup>
import Card from 'primevue/card';

import Button  from 'primevue/button';

import 'primeicons/primeicons.css'

</script>

<style scoped>
.content {
  padding: 20px;
}

h1 {
  text-align: center;
}

.card {
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.2);
}

.button {
  margin-top: 10px;
}
.hero-header{
  display:flex;
  justify-content:center;
  gap: 1rem;

}
.grid-stack{
  display:grid;
  grid-template-columns: repeat(3, 1fr);
  gap:2rem;
}
.icon{
  width:7rem;
}
.title{
  font-size:3rem;
  padding:1rem 0rem;
  margin:0rem;
}

.subtitle{
    font-size:2rem;
  color:var(--primary-color);
  margin :0;

}
header {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin: 4rem 0;
  padding:3rem 4rem;

}

header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url(../../public/bg.svg) center/cover;
  opacity: 0.2;
  z-index: -1;
      box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.7);
  border-radius:1rem;

}



</style>
