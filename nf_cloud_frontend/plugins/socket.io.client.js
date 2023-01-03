import io from 'socket.io-client'

export default ({ app }, inject) => {
    const socket = io(
        app.$config.nf_cloud_backend_ws_url,
        // {
        //   transports: ['websocket', 'polling'],
        // }
      )
    
      socket.on('error', (error) => {
        console.log("Error occured while trying to establish connection to ", app.$config.nf_cloud_backend_ws_url)
        console.error(error)
      })
    
      inject('socket', socket)
}
