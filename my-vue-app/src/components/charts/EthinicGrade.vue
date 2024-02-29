<template>
  <Chart type="bar" :data="chartData" :options="chartOptions" class="chart"/>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Chart from 'primevue/chart';

const chartData = ref({});
const chartOptions = ref({});

onMounted(async () => {
    const apiData = await fetchEthnicGroupData();
    chartData.value = setChartData(apiData);
    chartOptions.value = setChartOptions();
});

// Function to fetch chart data from the API
const fetchEthnicGroupData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/stacked-scores-by-ethnicity');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
};

// Function to set chart data based on API response
const setChartData = (apiData) => {
    // Labels should correspond to each score type
    const labels = ['Scores'];

    const backgroundColors = ['#42A5F5', '#66BB6A', '#FFA726'];

    // Ensure the data is structured correctly for Chart.js
    const datasets = apiData.datasets.map((dataset, index) => {
        return {
            ...dataset,
            backgroundColor: backgroundColors[index] // Use specific colors or the ones from apiData
        };
    });

    return {
        labels,
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
            beginAtZero: true,
            ticks: {
                color: textColorSecondary
            },
            grid: {
                color: surfaceBorder
            }
        }
    }
};
};
</script >
<style>
</style>