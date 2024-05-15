<script setup lang="ts">
import SelectInput from '@/components/ui/select-input.vue'
import { SelectItem } from '@/types/select-item'
import { useApi } from '@/composables/api'
import { ref } from 'vue'

interface AudioDevice {
    name: string
    index: number
}

defineProps<{
    deviceIndex: string | null
}>()
const emit = defineEmits<{
    (event: 'update:deviceIndex', newValue: string | null): void
}>()

const { fetchWithErrorNotification } = useApi()

const items = ref<SelectItem[]>([])
await updateDevices()

async function updateDevices() {
    const response = await fetchWithErrorNotification<AudioDevice[]>(
        '/recording-devices', {},
        'error while loading recording devices: '
    )

    if(response.data) {
        items.value = response.data.map(device => {
            return { label: device.name, name: `${device.index}` }
        })
    }
}
</script>

<template>
    <label class="flex-grow max-w-64 min-w-52">
        <div class="mb-1">
            recording device
        </div>
        <SelectInput
            placeholder="default"
            :items="items"
            :selected-item-name="deviceIndex"
            @update:selectedItemName="newIndex => emit('update:deviceIndex', newIndex)"
        />
    </label>
</template>
