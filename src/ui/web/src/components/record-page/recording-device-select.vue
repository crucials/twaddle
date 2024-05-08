<script setup lang="ts">
import SelectInput from '@/components/ui/select-input.vue'
import { useNotificationsStore } from '@/stores/notifications'
import { ref } from 'vue'
import { EelResponse } from '@/types/eel-response'
import { SelectItem } from '@/types/select-item'

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

const { showNotification } = useNotificationsStore()

const items = ref<SelectItem[]>([])
await updateDevices()

async function updateDevices() {
    const devicesResponse: EelResponse<AudioDevice[]> = await eel.getRecordingDevices()()
    
    if(devicesResponse.error || !devicesResponse.data) {
        const errorNotificationText = devicesResponse.error ?
            'failed to load input devices: ' + devicesResponse.error.explanation :
            'failed to load input devices'

        showNotification({
            type: 'error',
            text: errorNotificationText
        })

        return
    }

    items.value = devicesResponse.data.map(device => {
        return { label: device.name, name: `${device.index}` }
    })
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
