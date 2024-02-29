<template>
    <div class="">

        <h2 class="title">Subject Grades</h2>
        <div class="card-shadow">
            <!-- Show spinner when loading the SubjectsChart data -->
            <div v-if="isLoadingSubjectsChart" class="flex justify-content-center">
                <ProgressSpinner />
            </div>
            <!-- Show SubjectsChart once the data is loaded -->
            <div v-else>
                <SubjectsChart style="height:40vh" />
            </div>
        </div>

        <h2 class="title">Study Hours</h2>
        <div class="card-shadow">
            <div v-if="isLoadingEthnicChart" class="flex justify-content-center">
                <ProgressSpinner />
            </div>
            <div v-else>
                <StudyHours />
            </div>
        </div>

              <h2 class="title">Parent Education</h2>
        <div class="card-shadow">
            <div v-if="isLoadingEthnicChart" class="flex justify-content-center">
                <ProgressSpinner />
            </div>
            <div v-else>
                <ParentEducation />
            </div>
        </div>

      <h2 class="title">Bar charts</h2>
        <div class="card-shadow">
            <div v-if="isLoadingEthnicChart" class="flex justify-content-center">
                <ProgressSpinner />
            </div>
            <div v-else>
                <DynamicBar />
            </div>
        </div>


       <h2 class="title">Test Pie</h2>
        <div class="card-shadow">
            <div v-if="isLoadingEthnicChart" class="flex justify-content-center">
                <ProgressSpinner />
            </div>
            <div v-else>
                <TestPie />
            </div>
        </div>


      <h2 class="title">Score Overview</h2>
        <div class="card-shadow">
            <div v-if="isLoadingEthnicChart" class="flex justify-content-center">
                <ProgressSpinner />
            </div>
            <div v-else>
                <RadarChart />
            </div>
        </div>


    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import SubjectsChart from "@/components/charts/SubjectsChart.vue";
import TestPie from "@/components/charts/TestPie.vue";
import RadarChart from "@/components/charts/RadarChart.vue";
import ProgressSpinner from 'primevue/progressspinner';
import DynamicBar from "@/components/charts/DynamicBar.vue";
import StudyHours from "@/components/charts/StudyHours.vue";
import ParentEducation from "@/components/charts/ParentEducation.vue";

const isLoadingSubjectsChart = ref(true);
const isLoadingEthnicChart = ref(true);

onMounted(async () => {
    const startTime = Date.now();

    // Fetch data for both charts
    const apiData = await fetchChartData();
    console.log(apiData);
    chartData.value = setChartData(apiData);
    chartOptions.value = setChartOptions();

    const elapsedTime = Date.now() - startTime;
    const delay = Math.max(1000 - elapsedTime +10, 0); // Ensure at least 3 seconds

    // Set loading state to false after the delay
    setTimeout(() => {
        isLoadingSubjectsChart.value = false;
        isLoadingEthnicChart.value = false;
    }, delay);
});

const chartData = ref();
const chartOptions = ref();


// Function to fetch chart data from the API
const fetchChartData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/line-scores'); // Adjust the URL as needed
      console.log(response)
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
};

// Function to set chart data
const setChartData = (apiData) => {
    const documentStyle = getComputedStyle(document.documentElement);

    // Convert the data dictionaries to arrays for the chart
    const datasets = apiData.datasets.map(dataset => {
        // Create an array for scores from 0 to 100
        const scoresArray = Array.from({ length: 101 }, (_, i) => i);

        // Map the scores array to the dataset format
        const data = scoresArray.map(score => ({
            x: score,
            y: dataset.data[score] || 0 // Use the score frequency or 0 if not present
        }));

        return {
            ...dataset,
            data,
            borderColor: documentStyle.getPropertyValue('--' + dataset.label.toLowerCase().replace(' ', '-') + '-500')
        };
    });

    return {
        labels: Array.from({ length: 101 }, (_, i) => i.toString()), // Labels from 0 to 100
        datasets
    };
};


// Function to set chart options
const setChartOptions = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
    const surfaceBorder = documentStyle.getPropertyValue('--surface-border');

    return {
        maintainAspectRatio: false,
        aspectRatio: 0.6,
        plugins: {
            legend: {
                labels: {
                    color: textColor
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: textColorSecondary
                },
                grid: {
                    color: surfaceBorder
                }
            },
            y: {
                ticks: {
                    color: textColorSecondary
                },
                grid: {
                    color: surfaceBorder
                }
            }
        }
    };
}
</script>

<style>
.card{
    display:flex;
  flex-direction:column;

}


.card-shadow{
  width:60vw;
  height:auto;
  margin: 2rem auto;
  padding: 3rem;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #fff;
}
.chart {
  height:60vh;
}

.title{
margin:5rem 0rem 1rem 0rem;
}

</style>
