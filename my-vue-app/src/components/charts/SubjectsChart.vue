<template>

        <Chart type="line" :data="chartData" :options="chartOptions" class="chart" />

</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from 'primevue/chart';

onMounted(async () => {
    const apiData = await fetchChartData();
    console.log(apiData)
    chartData.value = setChartData(apiData);
    chartOptions.value = setChartOptions();
});

const chartData = ref();
const chartOptions = ref();

const fetchChartData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/line-scores');
      console.log(response)
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
.chart {
  height:60vh;
}
</style>
