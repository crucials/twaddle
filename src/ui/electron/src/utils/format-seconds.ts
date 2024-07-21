/**
 * converts seconds count to a 'HH:MM:SS' string, omits 'HH' (hours)
 * if hours count is 0
 * @returns 'HOURS:MINUTES:SECONDS' string 
 */
export function formatSeconds(seconds: number) {
    const date = new Date()
    date.setHours(0, 0, 0, 0)
    date.setMinutes(0)

    date.setSeconds(seconds)

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
}
