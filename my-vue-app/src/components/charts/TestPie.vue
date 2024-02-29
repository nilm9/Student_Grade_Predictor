<template>
    <div class=" flex justify-content-center">
        <Chart type="doughnut" :data="chartData" :options="chartOptions" class="w-full md:w-30rem" />
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from 'primevue/chart';

const chartData = ref();
const chartOptions = ref(null);

onMounted(async () => {
    chartData.value = await setChartData();
    chartOptions.value = setChartOptions();
});

const fetchTestPrepData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/prep-data');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
};

const setChartData = async () => {
    const testData = await fetchTestPrepData();

    const documentStyle = getComputedStyle(document.body);

    return {
        labels: ['Test Prep Completed', 'Test Prep Not Completed'],
        datasets: [
            {
                data: [testData.TestPrepCompleted, testData.TestPrepNotCompleted],
                backgroundColor: [documentStyle.getPropertyValue('--blue-500'), documentStyle.getPropertyValue('--yellow-500')],
                hoverBackgroundColor: [documentStyle.getPropertyValue('--blue-400'), documentStyle.getPropertyValue('--yellow-400')]
            }
        ]
    };
};

const setChartOptions = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');

    return {
        plugins: {
            legend: {
                labels: {
                    color: textColor
                }
            }
        },
        cutoutPercentage: 60
    };
};
</script>

<style>
.card {
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    margin: 20px;
}
</style>
