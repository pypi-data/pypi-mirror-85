import adbase as ad

import datetime

  - alias: Soveværelse tænd lys ved bevægelse
    trigger:
      platform: state
      entity_id: binary_sensor.bedroom_movement
      to: 'on'
    condition:
      - condition: state
        entity_id: sun.sun
        state: 'below_horizon'
      - condition: or
        conditions:
        - condition: state
          entity_id: input_boolean.kids
          state: 'off'
        - condition: and
          conditions:
          - condition: time
            after:  '12:00:00'
          - condition: state
            entity_id: input_boolean.kids_asleep
            state: 'off'        
    action:
      - service: light.turn_on
        entity_id: light.sovevrelseloft

  - alias: Soveværelse morgenlys ved bevægelse
    trigger:
      platform: state
      entity_id: binary_sensor.bedroom_movement
      to: 'on'
    condition:
      - condition: time
        after: '05:50:00'
        before: '09:00:00'
      - condition: state
        entity_id: input_boolean.kids
        state: 'off'
    action:
      - service: script.st_op_lys

  - alias: Soveværelse sluk uden bevægelse
    trigger:
      platform: state
      entity_id: binary_sensor.bedroom_movement
      to: 'off'
      for:
        minutes: 3
    condition:
      - condition: state
        entity_id: input_boolean.kids
        state: 'off'
    action:
      service: light.turn_off
      entity_id: light.sovevrelseloft
      data:
        transition: 240

  - alias: Soveværelse sluk uden bevægelse med børn
    trigger:
      platform: state
      entity_id: binary_sensor.bedroom_movement
      to: 'off'
      for:
        minutes: 15
    condition:
      - condition: state
        entity_id: input_boolean.kids
        state: 'on'
    action:
      service: light.turn_off
      entity_id: light.sovevrelseloft
      data:
        transition: 30



class Bedroom(ad.ADBase):
    def initialize(self):
        self.hass = self.get_plugin_api("HASS")
        self.mqtt = self.get_plugin_api("MQTT")

        self.light_id = self.args["light_id"]
        self.media_player_id = self.args["media_player_id"]
        self.movement_id = self.args["movement_id"]
        self.switch_unique_id = self.args["switch_unique_id"]
        self.kids_around_id = self.args["kids_around_id"]
        self.kids_asleep_id = self.args["kids_asleep_id"]

        self.hass.listen_event(self.switch_click, deconz_event, unique_id=self.switch_unique_id)

        self.hass.listen_state(
            self.movement_on_morning_kids,
            self.movement_id,
            new="on",
            constrain_input_boolean="input_boolean.kids",
            constrain_start_time="05:50:00",
            constrain_end_time="09:00:00"
        )

        self.hass.listen_state(
            self.movement_on,
            self.movement_id,
            new="on",
            constrain_start_time="sunset",
            constrain_end_time="sunrise + 00:30:00",
        )

        self.hass.listen_state(self.movement_off_tiny, self.movement_id, new="off", duration=5*60)
        self.hass.listen_state(self.movement_off_short, self.movement_id, new="off", duration=10*60)
        self.hass.listen_state(self.movement_off_long, self.movement_id, new="off", duration=20*60)


        self.mqtt.listen_event(self.switch_press, "MQTT_MESSAGE", topic=f"shellies/{self.switch_topic}/longpush/0")

        self.hass.listen_state(self.movement_on, self.movement_id, new="on")

        self.hass.listen_state(self.movement_off_short, self.movement_id, new="off", duration=5*60)
        self.hass.listen_state(self.movement_off_long, self.movement_id, new="off", duration=15*60)

    def switch_click(self, event_name, data, kwargs):
        self.log(f"__function__ - data:{data}")
        if data["event"] == 1002:     # left
            state = self.get_state(self.left_light_id)
            if state == "on":
                self.turn_off(self.left_light_id)
                self.left_force_off = True
            else:
                if self.left_force_off:
                    self.call_service("light/turn_on", entity_id=self.left_light_id, kelvin=3500, brightness_pct=35)
                else:
                    self.turn_on(self.left_light_id)
        elif data["event"] == 2002:   # right
            self.toggle(self.right_light_id)
        elif data["event"] == 3002:   # both
            self.call_service("media_player/media_pause", entity_id=self.media_player_id)

    def turn_on(self):
        kids_asleep = (self.hass.get_state("input_boolean.kids_asleep") == "on")

        if kids_asleep and self.hass.now_is_between("01:00:00", "05:00:00"):
            attrs = { 'kelvin': 2200, 'brightness_pct': 10 }
        elif self.hass.now_is_between("23:00:00", "06:00:00"):
            attrs = { 'kelvin': 2500, 'brightness_pct': 25 }
        elif self.hass.now_is_between("06:00:00", "07:00:00"):
            attrs = { 'kelvin': 3500, 'brightness_pct': 35 }
        elif self.hass.now_is_between("06:45:00", "09:00:00"):
            attrs = { 'kelvin': 3500, 'brightness_pct': 70 }
            if self.hass.get_state("sun.sun", attribute="elevation") < 10:
                self.hass.call_service("light/turn_on", entity_id=self.ceiling_id)
        elif self.hass.now_is_between("21:00:00", "23:00:00"):
            attrs = { 'kelvin': 3500, 'brightness_pct': 50 }
        else:
            attrs = { 'kelvin': 3500, 'brightness_pct': 65 }

        self.hass.call_service("light/turn_on", entity_id=[self.left_id, self.right_id], **attrs)

    def turn_off(self, transition=0.25):
        self.hass.call_service("light/turn_off", entity_id=[self.left_id, self.right_id, self.ceiling_id], transition=transition)

    def movement_on(self, entity, attributes, old, new, kwargs):
        self.hass.log(f"__function__ - old:{old} new:{new}")
        self.switch_time = datetime.datetime.now()

        self.turn_on()

    def movement_off_short(self, entity, attributes, old, new, kwargs):
        self.hass.log(f"__function__")
        self.turn_off(transition=120)

    def movement_off_long(self, entity, attributes, old, new, kwargs):
        self.hass.log(f"__function__")
