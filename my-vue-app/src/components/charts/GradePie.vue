<template>
  <div class=" flex justify-content-center">
    <Chart type="pie" :data="chartData" :options="chartOptions" class="w-full md:w-30rem" />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

onMounted(() => {
    chartData.value = setChartData();
    chartOptions.value = setChartOptions();
});

const chartData = ref();
const chartOptions = ref();

const setChartData = () => {
    const documentStyle = getComputedStyle(document.body);
    const total = 1000; // Assuming a total of 1000 to calculate values from percentages
    return {
        labels: ['A', 'B', 'C', 'D', 'F'],
        datasets: [
            {
                data: [
                  total * 6.79 / 100,
                  total * 15.60 / 100,
                  total * 23.64 / 100,
                  total * 25.38 / 100,
                  total * 28.58 / 100
                ],
                backgroundColor: [
                  documentStyle.getPropertyValue('--green-500'),
                  documentStyle.getPropertyValue('--yellow-500'),
                  documentStyle.getPropertyValue('--orange-500'),
                  documentStyle.getPropertyValue('--blue-500'),
                  documentStyle.getPropertyValue('--red-500')
                ],
                hoverBackgroundColor: [
                  documentStyle.getPropertyValue('--green-400'),
                  documentStyle.getPropertyValue('--yellow-400'),
                  documentStyle.getPropertyValue('--orange-400'),
                  documentStyle.getPropertyValue('--blue-400'),
                  documentStyle.getPropertyValue('--red-400')
                ]
            }
        ]
    };
};

const setChartOptions = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');
    return {
        plugins: {
            legend: {
                labels: {
                    usePointStyle: true,
                    color: textColor
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.label || '';
                        if (label) {
                            label += ': ';
                        }

                        return label;
                    }
                }
            }
        }
    };
};
</script>
