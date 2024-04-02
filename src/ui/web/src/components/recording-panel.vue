<script setup lang="ts">
import FilledButton from '@/components/ui/filled-button.vue'
import CustomTable from '@/components/custom-table.vue'
import { ref, computed, reactive } from 'vue'
import TextInput from '@/components/ui/text-input.vue';

const props = defineProps<{
    secondsPassed: number
    wordsCountValues: Record<string, number>
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
    tableExpanded: false,
})

const result = computed(() => {
    const wordCountValues = Object.keys(props.wordsCountValues).map(word => ({
        word: word,
        count: props.wordsCountValues[word]
    }))

    if(resultViewOptions.tableExpanded) {
        return wordCountValues
    }
    else {
        return wordCountValues.slice(0, 10)
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

            <form class="flex items-center gap-7 mb-8">
                <TextInput
                    v-model="resultViewOptions.searchText" 
                    placeholder="search word"
                />
            </form>

            <CustomTable
                :items="result"
                class="w-1/2 mb-4"
            />

            <button class="hover:text-neutral-700 font-medium" @click="resultViewOptions.tableExpanded = !resultViewOptions.tableExpanded">
                expand
            </button>
        </section>
    </div>
</template>
