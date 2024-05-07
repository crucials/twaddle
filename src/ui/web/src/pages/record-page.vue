<script setup lang="ts">
import StartRecordingPanel from '@/components/start-recording-panel.vue'
</script>

<template>
    <main class="flex-grow p-6 pt-0">
        <p class="text-lg font-normal max-w-[900px] mb-10">
            this app records your speech, transcribes it and provides a list of words that you said with the usage
            count. needed words can be specified
        </p>

        <StartRecordingPanel />
    </main>
</template>
