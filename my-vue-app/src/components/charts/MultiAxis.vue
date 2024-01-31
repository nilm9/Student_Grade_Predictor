<template>
    <div class="card">
        <Chart type="line" :data="chartData" :options="chartOptions" class="h-30rem" />
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from 'primevue/chart';

const chartData = ref();
const chartOptions = ref();
onMounted(async () => {
    const apiData = await fetchMultiAxisChartData();
    if (apiData) {
        chartData.value = setChartData(apiData);
        chartOptions.value = setChartOptions();
    }
});

const fetchMultiAxisChartData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/multi-axis-chart-data');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
};

const setChartData = (apiData) => {
    const documentStyle = getComputedStyle(document.documentElement);

    return {
        labels: apiData.labels,
        datasets: [
            {
                ...apiData.datasets[0],
                borderColor: documentStyle.getPropertyValue('--blue-500'),
                pointBackgroundColor: documentStyle.getPropertyValue('--blue-500'),
                tension: 0.4
            },
            // Add other dataset(s) for additional axes here if needed
        ]
    };
};

const setChartOptions = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
    const surfaceBorder = documentStyle.getPropertyValue('--surface-border');

    return {
        stacked: false,
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
                type: 'linear',
                display: true,
                position: 'left',
                ticks: {
                    color: textColorSecondary
                },
                grid: {
                    color: surfaceBorder
                }
            },
            // Add configuration for the second y-axis (y1) if you have a second dataset
            // y1: { ... }
        }
    };
}
</script>

<style>
/* Add your component-specific styles here */
.card {
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    margin: 20px;
}
</style>
