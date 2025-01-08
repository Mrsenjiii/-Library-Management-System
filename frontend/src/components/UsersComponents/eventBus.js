// eventBus.js
import { createApp } from 'vue';
console.log('Event Bus initialized');

const eventBus = createApp({});
eventBus.config.globalProperties.eventBus = eventBus;

export default eventBus;