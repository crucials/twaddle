<script setup lang="ts">
import SelectInput from '@/components/ui/select-input.vue'
import WordListSelect from '@/components/word-list-select.vue'
import { supportedLanguages } from '@/supported-languages.ts'

defineProps<{
    wordListName: string | null
    language: string | null
}>()
const emit = defineEmits<{
    (event: 'update:wordListName', newWordList: string | null): void,
    (event: 'update:language', newLanguage: string | null): void,
}>()
</script>

<template>
    <WordListSelect
        :list-name="wordListName"
        @update:list-name="newValue => emit('update:wordListName', newValue)"
    />

    <label class="flex-grow max-w-64 min-w-52">
        <div class="mb-1">
            speech language
        </div>
        <SelectInput
            :items="Object.keys(supportedLanguages).map(languageCode => ({
                name: languageCode, label: supportedLanguages[languageCode]
            }))"
            searchable
            placeholder="auto-detect"
            :selected-item-name="language"
            @update:selected-item-name="newValue => emit('update:language', newValue)"
        />
    </label>
</template>
