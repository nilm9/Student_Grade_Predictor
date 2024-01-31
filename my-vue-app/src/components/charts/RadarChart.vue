<template>
    <div class=" flex justify-content-center">
        <Chart type="radar" :data="chartData" :options="chartOptions" class="w-full md:w-30rem" />
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from 'primevue/chart';

const chartData = ref();
const chartOptions = ref();

onMounted(async () => {
    chartData.value = await fetchRadarChartData();
    chartOptions.value = setChartOptions();
});

const fetchRadarChartData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/radar-chart-data');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
};

const setChartOptions = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');

    return {
        plugins: {
            legend: {
                labels: {
                    color: textColor
                }
            }
        },
        scales: {
            r: {
                grid: {
                    color: textColorSecondary
                }
            }
        }
    };
}
</script>

<style>
/* Add your component-specific styles here */

</style>
