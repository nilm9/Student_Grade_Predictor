<template>
    <div class="dashboard ">
        <div class="dashboard-row card">
            <div class="dashboard-item" style="width:45vw;height:35vh;" >
                        <SubjectsChart class="chart"  />
            </div>

            <div class="dashboard-item"  style="width:40vw;height:40vh;">

                        <TestPie class="chart"/>

            </div>


        <!-- Repeat for other rows and charts -->
        <!-- Example: -->
            <div class="dashboard-item" style="width:35vw;height:35vh;">

                        <RadarChart class="chart"/>
            </div>

            <div class="dashboard-item" style="width:35vw;height:35vh;">
                        <StudyHours  class="chart"/>

                </div>
        </div>

        <!-- Add more rows as needed -->
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";



import SubjectsChart from "@/components/charts/SubjectsChart.vue";
//import EthnicGrades from "@/components/charts/EthinicGrade.vue";

//import GradePie from "@/components/charts/GradePie.vue";

import TestPie from "@/components/charts/TestPie.vue";
import RadarChart from "@/components/charts/RadarChart.vue";
import StudyHours from "@/components/charts/StudyHours.vue";


//import DynamicBar from "@/components/charts/DynamicBar.vue";

const isLoadingSubjectsChart = ref(true);
const isLoadingEthnicChart = ref(true);

// Sample onMounted logic
onMounted(async () => {
    // Mock delay for loading data
    setTimeout(() => {
        isLoadingSubjectsChart.value = false;
        isLoadingEthnicChart.value = false;
    }, 2000);
});
</script>

<style>
.dashboard {
    display: flex;
  align-items:center;
    justify-content: center;
margin:3rem 5rem;    gap: 1rem
}

.dashboard-row {
    display: grid;
  grid-template-columns:repeat(2, 1fr);
}

.dashboard-item {
}

.card-shadow {
    padding: 1rem;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    background-color: #fff;
}

.title {
    margin-bottom: 1rem;
}

.flex.justify-content-center {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 300px; /* Adjust based on your needs */
}
.chart {
  height:inherit;
  padding: .25rem;
}

.card {
    /* Example styling for the card */
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    margin: 20px;
}
</style>
