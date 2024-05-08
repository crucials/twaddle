<script setup lang="ts">
import FilledButton from '@/components/ui/filled-button.vue'
import CustomTable from '@/components/custom-table.vue'
import TextInput from '@/components/ui/text-input.vue'
import SheetDialog from '@/components/ui/sheet-dialog.vue'

import { ref, computed, reactive } from 'vue'
import { SpokenWordStats } from '@/types/spoken-word-stats'

const props = defineProps<{
    secondsPassed: number
    spokenWordStats: SpokenWordStats[]
    fullText: string
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

const resultViewOptions = reactive({
    searchText: '',
    tableExpanded: false
})

const filteredAndSortedResult = computed(() => {
    const filteredResult = props.spokenWordStats.filter(stats => {
        return stats.word.toUpperCase()
            .includes(resultViewOptions.searchText.toUpperCase().trim())
    })
    filteredResult.sort((stats1, stats2) => stats2.count - stats1.count)

    return filteredResult
})

const SHRINKED_TABLE_ROWS = 12
const shrinkedResult = computed(() => {
    if(resultViewOptions.tableExpanded) {
        return filteredAndSortedResult.value
    }
    else {
        return filteredAndSortedResult.value.slice(0, SHRINKED_TABLE_ROWS)
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

        <section>
            <h2 class="text-2xl font-bold tracking-wide mb-6">
                result
            </h2>

           <div v-if="spokenWordStats.length > 0">
                <p class="text-neutral-500 mb-3">
                    {{ spokenWordStats.length }} words.
                </p>

                <SheetDialog heading="full text" trigger-button-container-class="mb-5">
                    <template #triggerButton>
                        <FilledButton>
                            view full text
                        </FilledButton>
                    </template>

                    <template #default>
                        {{ fullText }}
                    </template>
                </SheetDialog>

                <form class="flex items-center gap-7 mb-6">
                    <TextInput
                        v-model="resultViewOptions.searchText" 
                        placeholder="search word"
                    />
                </form>

                <button
                    v-if="resultViewOptions.tableExpanded
                        && filteredAndSortedResult.length > SHRINKED_TABLE_ROWS"
                    class="transition-colors duration-200 font-medium text-lg
                        p-2 rounded-md hover:bg-neutral-200
                        flex items-center gap-x-2 mb-4"
                    @click="resultViewOptions.tableExpanded = false"
                >
                    <svg class="w-6 rotate-180" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
                        <path d="M18 18L12 12L6 18" class="stroke-neutral-800" stroke-width="2"/>
                        <path d="M18 12L12 6L6 12" class="stroke-neutral-800" stroke-width="2"/>
                    </svg>
                    show less
                </button>

                <CustomTable
                    :items="shrinkedResult"
                    class="w-1/2 mb-4"
                />

                <button
                    v-if="!resultViewOptions.tableExpanded
                        && filteredAndSortedResult.length > SHRINKED_TABLE_ROWS"
                    class="transition-colors duration-200 font-medium text-lg
                        p-2 rounded-md hover:bg-neutral-200 
                        flex items-center gap-x-2"
                    @click="resultViewOptions.tableExpanded = true"
                >
                    <svg class="w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
                        <path d="M18 18L12 12L6 18" class="stroke-neutral-800" stroke-width="2"/>
                        <path d="M18 12L12 6L6 12" class="stroke-neutral-800" stroke-width="2"/>
                    </svg>
                    show more
                </button>
           </div>

           <p v-else class="text-neutral-500">
                words count table will appear here after ~10 seconds, when the first
                transcription happens
           </p>
        </section>
    </div>
</template>
