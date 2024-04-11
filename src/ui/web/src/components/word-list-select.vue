<script setup lang="ts">
import SelectInput from '@/components/ui/select-input.vue'
import { useNotificationsStore } from '@/stores/notifications'
import { EelResponse } from '@/types/eel-response';
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
    (event: 'update:listName', newName: string): void
}>()

const { showNotification } = useNotificationsStore()

const items = ref<SelectItem[]>([])
await updateWordLists()

async function updateWordLists() {
    const response: EelResponse<WordList[]> = await eel.getWordLists()()
    console.log(response)

    if(response.error || !response.data) {
        const errorNotificationText = response.error ?
            'failed to load word lists: ' + response.error.explanation :
            'failed to load word lists'

        showNotification({
            type: 'error',
            text: errorNotificationText
        })

        return
    }

    items.value = response.data.map(wordList => {
        return { label: wordList.name, name: wordList.name }
    })

    console.log(items.value)
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
            @update:selectedItemName="(newName: string) => emit('update:listName', newName)"
        />
    </label>
</template>
