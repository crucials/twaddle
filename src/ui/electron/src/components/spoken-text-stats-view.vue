<script setup lang="ts">
import CustomTable from '@/components/custom-table.vue'
import TextInput from '@/components/ui/text-input.vue'
import SheetDialog from '@/components/ui/sheet-dialog.vue'
import FilledButton from '@/components/ui/filled-button.vue'
import TextIcon from '@/components/ui/icons/text-icon.vue'
import ExportButton from '@/components/export-button.vue'
import { SpokenTextStats } from '@/types/spoken-text-stats'
import { computed, reactive } from 'vue'

const props = defineProps<{
    stats: SpokenTextStats
}>()

const viewOptions = reactive({
    searchText: '',
    tableExpanded: false
})

const filteredAndSortedStats = computed(() => {
    const filteredResult = props.stats.wordsStats.filter(stats => {
        return stats.word.toUpperCase()
            .includes(viewOptions.searchText.toUpperCase().trim())
    })
    filteredResult.sort((stats1, stats2) => stats2.count - stats1.count)

    return filteredResult
})

const SHRINKED_TABLE_ROWS = 12
const shrinkedStats = computed(() => {
    if(viewOptions.tableExpanded) {
        return filteredAndSortedStats.value
    }
    else {
        return filteredAndSortedStats.value.slice(0, SHRINKED_TABLE_ROWS)
    }
})
</script>

<template>
    <section>
        <h2 class="text-2xl font-bold tracking-wide mb-8">
            result
        </h2>

        <div class="flex items-stretch gap-x-2 mb-6">
            <SheetDialog heading="full text">
                <template #triggerButton>
                    <FilledButton>
                        <TextIcon class="w-6" />
                        view full text
                    </FilledButton>
                </template>

                <template #default>
                    {{ stats.fullText }}
                </template>
            </SheetDialog>

            <ExportButton :stats-to-export="stats" />
        </div>

        <hr class="w-full max-w-96 bg-neutral-300 h-px border-none mb-6">

        <div v-if="stats.wordsStats.length > 0">
            <p class="text-neutral-500 mb-3">
                {{ stats.wordsStats.length }} words
            </p>

            <form class="flex items-center gap-7 mb-6">
                <TextInput
                    v-model="viewOptions.searchText" 
                    placeholder="search word"
                />
            </form>

            <button
                v-if="viewOptions.tableExpanded
                    && filteredAndSortedStats.length > SHRINKED_TABLE_ROWS"
                class="transition-colors duration-200 font-medium text-lg
                    p-2 rounded-md hover:bg-neutral-200
                    flex items-center gap-x-2 mb-4"
                @click="viewOptions.tableExpanded = false"
            >
                <svg class="w-6 rotate-180" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
                    <path d="M18 18L12 12L6 18" class="stroke-neutral-800" stroke-width="2"/>
                    <path d="M18 12L12 6L6 12" class="stroke-neutral-800" stroke-width="2"/>
                </svg>
                show less
            </button>

            <CustomTable
                :items="shrinkedStats"
                class="w-1/2 mb-4"
            />

            <button
                v-if="!viewOptions.tableExpanded
                    && filteredAndSortedStats.length > SHRINKED_TABLE_ROWS"
                class="transition-colors duration-200 font-medium text-lg
                    p-2 rounded-md hover:bg-neutral-200 
                    flex items-center gap-x-2"
                @click="viewOptions.tableExpanded = true"
            >
                <svg class="w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
                    <path d="M18 18L12 12L6 18" class="stroke-neutral-800" stroke-width="2"/>
                    <path d="M18 12L12 6L6 12" class="stroke-neutral-800" stroke-width="2"/>
                </svg>
                show more
            </button>
        </div>

        <p v-else class="text-neutral-500">
            <slot name="no-words-fallback"></slot>
        </p>
    </section>
</template>
