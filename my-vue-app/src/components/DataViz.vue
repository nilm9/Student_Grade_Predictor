<template>
    <div class="card">
        <Chart type="line" :data="chartData" :options="chartOptions" class="h-30rem" />
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const chartData = ref();
const chartOptions = ref(setChartOptions());

onMounted(async () => {
    try {
        const response = await axios.get('/api/chart/line-scores');
        chartData.value = adaptChartData(response.data);
    } catch (error) {
        console.error('Error fetching line scores data:', error);
    }
});

const adaptChartData = (apiData) => {
    const documentStyle = getComputedStyle(document.documentElement);

    return {
        labels: apiData.labels,
        datasets: [
            {
                label: 'Math Score',
                data: apiData.datasets[0].data,
                fill: false,
                tension: 0.4,
                borderColor: documentStyle.getPropertyValue('--blue-500')
            },
            {
                label: 'Reading Score',
                data: apiData.datasets[1].data,
                fill: false,
                borderDash: [5, 5],
                tension: 0.4,
                borderColor: documentStyle.getPropertyValue('--teal-500')
            },
            {
                label: 'Writing Score',
                data: apiData.datasets[2].data,
                fill: true,
                borderColor: documentStyle.getPropertyValue('--orange-500'),
                tension: 0.4,
                backgroundColor: 'rgba(255,167,38,0.2)'
            }
        ]
    };
};

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
