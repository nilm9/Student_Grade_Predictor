<template>
  <div>
    <Dropdown :options="features" v-model="selectedFeature" @change="fetchAndDisplayData" />
    <Chart type="bar" :data="chartData" :options="chartOptions" class="chart" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Chart from 'primevue/chart';
import Dropdown from 'primevue/dropdown';

const chartData = ref(null);
const chartOptions = ref({});
const featureMapping = {
 'Lunch Type Standard': 'LunchType_standard',
  'Is Gender Male': 'Gender_male',

    'Test Preparation ': ['TestPrep_completed', 'TestPrep_none'],
    'Parents Married': ['ParentMaritalStatus_divorced', 'ParentMaritalStatus_married', 'ParentMaritalStatus_single', 'ParentMaritalStatus_widowed'],
    'Transport Means Private': ['TransportMeans_private', 'TransportMeans_school_bus']
};
const features = ref(Object.keys(featureMapping));
// Set a default value for selectedFeature
const selectedFeature = ref('Lunch Type Standard');

onMounted(async () => {
    chartOptions.value = setChartOptions();
    await fetchAndDisplayData(); // Fetch data for the default selected feature
});

const fetchAndDisplayData = async () => {
    if (!selectedFeature.value) return;

    let dbFields = featureMapping[selectedFeature.value];
    if (!Array.isArray(dbFields)) {
        dbFields = [dbFields];
    }

    for (const field of dbFields) {
        try {
            const apiData = await fetchData(field);
            chartData.value = setChartData(apiData, field);
        } catch (error) {
            console.error('Error in fetching data:', error);
        }
    }
};
const fetchData = async (feature) => {
    // Replace with your actual API endpoint
    const response = await fetch(`http://127.0.0.1:5000/api/data_feature?feature=${feature}`);
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return await response.json();
};

const setChartData = (apiData, feature) => {
    const labels = Object.keys(apiData);
    const dataValues = Object.values(apiData);

    // Check if the data is binary
    const isBinaryData = labels.every(label => label === 'true' || label === 'false');

    let chartLabels, chartDataValues;

    if (isBinaryData) {
        // For binary data, use 'Yes' and 'No' labels
        chartLabels = ['Yes', 'No'];
        chartDataValues = [apiData['true'] || 0, apiData['false'] || 0];
    } else {
        // For non-binary data, use the labels and values as they are
        chartLabels = labels;
        chartDataValues = dataValues;
    }

    return {
        labels: chartLabels,
        datasets: [{
            label: `${feature} Data`,
            data: chartDataValues,
            backgroundColor: ['rgba(32,150,243,.2)', /* other colors */],
            borderColor: ['rgba(32,150,243,255)', /* other colors */],
            borderWidth: 1
        }]
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
    height: 400px;
    width: 100%;
}
</style>
