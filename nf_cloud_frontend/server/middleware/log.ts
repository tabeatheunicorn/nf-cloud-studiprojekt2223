export default defineEventHandler((event) => {
    console.log('New request: ' + event.req.url)
  })

function defineEventHandler(arg0: (event: any) => void) {
    throw new Error("Function not implemented.")
}
  