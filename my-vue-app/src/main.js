import { createApp } from 'vue';
import App from './App.vue';
import PrimeVue from 'primevue/config';

// Import PrimeVue styles
import 'primevue/resources/themes/saga-blue/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';


const app = createApp(App);

app.use(PrimeVue);

app.mount('#app');
