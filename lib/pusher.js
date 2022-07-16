class Pusher {
  constructor(HOST, PORT) {
    this.websocket = new WebSocket(`ws://${HOST}:${PORT}`)
    this.events = {}

    this.websocket.addEventListener("message", ({data}) => {
      var event = JSON.parse(data);

      if(event._channel_name in this.events){
        if(event._event_type in this.events[event._channel_name]){
          for (var i = 0; i < this.events[event._channel_name][event._event_type].length; i++) {
            this.events[event._channel_name][event._event_type][i](event)
          }
        }
      }
    });

    this.websocket.addEventListener("open", () => console.log("connection"))
  }

  subscribe(name){
    this.websocket.send(JSON.stringify({
      server_response: true,
      type: "connect",
      channel_name: name
    }))

    return new Channel(this, name)
  }

  add_event(channel, event, func){
    if(!this.events[channel]) this.events[channel] = {};
    if(!this.events[channel][event]) this.events[channel][event] = [];
    this.events[channel][event].push(func)
    console.log(this.events);
  }

}


class Channel {
  constructor(pusher, name) {
    this.pusher = pusher
    this.name = name
  }

  bind(event, func){
    pusher.add_event(this.name, event, func)
  }
}
