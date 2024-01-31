<template>
  <div>
    <Chart type="bar" :data="chartData" :options="chartOptions" class="chart" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Chart from 'primevue/chart';

const chartData = ref(null);
const chartOptions = ref({});

onMounted(async () => {
    chartOptions.value = setChartOptions();
    await fetchAndDisplayData();
});

const fetchAndDisplayData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/feature-importance');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        chartData.value = setChartData(data.feature_importance);
    } catch (error) {
        console.error('Error in fetching data:', error);
    }
};

const setChartData = (featureImportances) => {
    const labels = featureImportances.map(item => item[0]);
    const dataValues = featureImportances.map(item => item[1]);

    return {
        labels: labels,
        datasets: [{
            label: 'Feature Importances',
            data: dataValues,
            backgroundColor: 'rgba(32, 150, 243, 0.2)',
            borderColor: 'rgba(32, 150, 243, 1)',
            borderWidth: 1
        }]
    };
};

const setChartOptions = () => {
    return {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    };
}
</script>

<style>
.chart {
    height: 400px;
    width: 100%;
}
</style>
