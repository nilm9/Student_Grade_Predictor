<template>
    <div class="">
        <Chart type="bar" :data="chartData" :options="chartOptions" />
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from 'primevue/chart';

const chartData = ref(null);
const chartOptions = ref(null);

onMounted(async () => {
    await fetchStudyHoursData();
    chartOptions.value = setChartOptions();
});

const fetchStudyHoursData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/study-hours-distribution');
        if (!response.ok) throw new Error('Failed to fetch data');
        const data = await response.json();
        chartData.value = setChartData(data);
    } catch (error) {
        console.error('Error:', error);
    }
};



const setChartData = (apiData) => {
    // New labels for the categories
    const newLabels = ["<5h", "5h-10h", ">10h", "Unknown"];

    // Array from API response
    const apiDataArray = Object.values(apiData);

    // Map the API data directly to new labels based on array positions
    const transformedData = newLabels.map((label, index) => {
        return apiDataArray[index] || 0; // Use the value at the corresponding index or default to 0
    });

    // Return the transformed chart data
    return {
        labels: newLabels,
        datasets: [
            {
                label: 'Weekly Study Hours Distribution',
                data: transformedData,
                backgroundColor: ['rgba(54, 162, 235, 0.5)', 'rgba(75, 192, 192, 0.5)', 'rgba(255, 206, 86, 0.5)', 'rgba(201, 203, 207, 0.5)'],
                borderColor: ['rgb(54, 162, 235)', 'rgb(75, 192, 192)', 'rgb(255, 206, 86)', 'rgb(201, 203, 207)'],
                borderWidth: 1
            }
        ]
    };
};

const setChartOptions = () => {
    return {
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Weekly Study Hours'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Number of Students'
                }
            }
        }
    };
};
</script>
