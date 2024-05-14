<script setup lang="ts">
import FilledButton from '@/components/ui/filled-button.vue'

import { computed, reactive } from 'vue'
import { SpokenTextStats } from '@/types/spoken-text-stats'
import SpokenTextStatsView from '@/components/spoken-text-stats-view.vue'

const props = defineProps<{
    secondsPassed: number
    result: SpokenTextStats
}>()
const emit = defineEmits<{
    (event: 'reset'): void
}>()

const timer = computed(() => {
    const date = new Date()
    date.setHours(0, 0, 0, 0)
    date.setMinutes(0)

    date.setSeconds(props.secondsPassed)

    const hours = `${date.getHours()}`.padStart(2, '0')
    const minutesAndSeconds = date.toLocaleTimeString(undefined, {
        minute: '2-digit', second: '2-digit'
    })

    if(hours === '00') {
        return minutesAndSeconds
    }
    else {
        return hours + ':' + minutesAndSeconds
    }
})
</script>

<template>
    <div
        class="bg-neutral-100 rounded-lg max-w-[1080px] px-8 py-7 min-h-72"
    >
        <div class="flex items-center gap-x-12 mb-10">
            <time :datetime="timer" class="block text-neutral-400 font-medium text-5xl">
                {{ timer }}
            </time>

            <FilledButton @click="emit('reset')">
                reset
            </FilledButton>
        </div>

        <SpokenTextStatsView :stats="result" />
    </div>
</template>
