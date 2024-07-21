<script setup lang="ts">
import FilledButton from '@/components/ui/filled-button.vue'
import SpokenTextStatsView from '@/components/spoken-text-stats-view.vue'
import { SpokenTextStats } from '@/types/spoken-text-stats'
import { formatSeconds } from '@/utils/format-seconds'
import { computed } from 'vue'

const props = defineProps<{
    secondsPassed: number
    result: SpokenTextStats
}>()
const emit = defineEmits<{
    (event: 'reset'): void
}>()

const timer = computed(() => formatSeconds(props.secondsPassed))
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

        <SpokenTextStatsView :stats="result" :seconds-speaking="secondsPassed">
            <template #no-words-fallback>
                words count table will appear here after ~10 seconds, 
                when the first transcription happens
                <br>
                if table is not appearing, spoken words are either not in
                the selected word list or can't be detected
            </template>
        </SpokenTextStatsView>
    </div>
</template>
