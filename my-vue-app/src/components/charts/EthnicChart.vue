<template>
    <div class="card">
        <Chart type="bar" :data="chartData" :options="chartOptions" class="chart"/>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from 'primevue/chart'; // Replace with your actual Chart component import

const chartData = ref();
const chartOptions = ref();

onMounted(async () => {
    const apiData = await fetchEthnicGroupData();
    chartData.value = setChartData(apiData);
    chartOptions.value = setChartOptions();
});

// Function to fetch chart data from the API
const fetchEthnicGroupData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/ethnic-group-data'); // Adjust the URL as needed
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
    // Extracting the labels (ethnic groups) and their counts
    const labels = Object.keys(apiData);
    const datasets = [{
        label: 'Ethnic Group Count',
        data: labels.map(label => apiData[label][label]), // Assuming the count is stored as value of the same key
        backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)'],
        borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)'],
        borderWidth: 1
    }];

    return {
        labels,
        datasets
    };
};

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
}
</script>



<style>

.chart {
  height:60vh;
  width:40vw;
}
</style>

