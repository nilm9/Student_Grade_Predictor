<template>
    <div class="">
        <Chart type="line" :data="chartData" :options="chartOptions" class="h-30rem" />
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from 'primevue/chart';

const chartData = ref(null);
const chartOptions = ref(null);

onMounted(() => {
    fetchChartData();
});
const fetchChartData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/multi-axis-chart-data');
        if (response.ok) {
            const data = await response.json();
            console.log("Original Data:", data); // Debug original data
            chartData.value = transformChartData(data);
            chartOptions.value = setChartOptions();
        } else {
            console.error('Failed to fetch chart data');
        }
    } catch (error) {
        console.error('Error fetching chart data:', error);
    }
};

const transformChartData = (data) => {
    // New labels for the categories
    const newLabels = ["<5h", "5h-10h", ">10h", "Unknown"];

    // Initialize array for 4 categories
    const transformedData = [0, 0, 0, 0];

    // Iterate over the object and aggregate the values into the new categories
    for (const [hours, count] of Object.entries(data)) {
        const numHours = parseInt(hours);

        if (!isNaN(numHours)) {
            if (numHours < 5) {
                transformedData[0] += count; // Increment <5h category
            } else if (numHours >= 5 && numHours <= 10) {
                transformedData[1] += count; // Increment 5h-10h category
            } else {
                transformedData[2] += count; // Increment >10h category
            }
        } else {
            transformedData[3] += count; // Increment Unknown category for non-numeric hours
        }
    }

    // Return the transformed chart data
    return {
        labels: newLabels,
        datasets: [
            {
                label: 'Weekly Study Hours',
                data: transformedData,
                backgroundColor: ['#42A5F5', '#66BB6A', '#FFA726', '#FFC107'], // Example colors
                fill: false,
                tension: 0.4
            }
        ]
    };
};
const setChartOptions = () => {
    return {
        maintainAspectRatio: false,
        scales: {
            y: {
                type: 'linear',
                display: true,
                position: 'left',
            },
            y2: {
                type: 'linear',
                display: true,
                position: 'right',
                grid: {
                    drawOnChartArea: false
                },
            }
        }
    };
}
</script>

<style scoped>
.card {
    padding: 1rem;
}
</style>
