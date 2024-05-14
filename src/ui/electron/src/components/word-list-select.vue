<script setup lang="ts">
import SelectInput from '@/components/ui/select-input.vue'
import { useApi } from '@/composables/api';
import { SelectItem } from '@/types/select-item'
import { ref } from 'vue'

interface WordList {
    name: string
    words: string[]
}

defineProps<{
    listName: string | null;
}>()
const emit = defineEmits<{
    (event: 'update:listName', newName: string | null): void
}>()

const { fetchWithErrorNotification } = useApi()

const items = ref<SelectItem[]>([])
await updateWordLists()

async function updateWordLists() {
    const response = await fetchWithErrorNotification<WordList[]>(
        '/word-lists', {},
        'error while loading word lists: '
    )

    if(response.data) {
        items.value = response.data.map(wordList => {
            return { label: wordList.name, name: wordList.name }
        })
    }
}
</script>

<template>
    <label class="flex-grow max-w-64 min-w-52">
        <div class="mb-1">
            words to count
        </div>
        <SelectInput
            placeholder="all"
            :items="items"
            :selected-item-name="listName"
            @update:selectedItemName="newName => emit('update:listName', newName)"
        />
    </label>
</template>
