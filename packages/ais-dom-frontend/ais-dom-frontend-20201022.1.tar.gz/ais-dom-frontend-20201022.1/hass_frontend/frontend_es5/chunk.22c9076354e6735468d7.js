(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[3386],{58763:function(e,t,r){"use strict";r.d(t,{vq:function(){return u},_J:function(){return d},Nu:function(){return h}});var n=r(29171),i=r(22311),a=r(91741);function o(e,t){var r;if("undefined"==typeof Symbol||null==e[Symbol.iterator]){if(Array.isArray(e)||(r=function(e,t){if(!e)return;if("string"==typeof e)return s(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return s(e,t)}(e))||t&&e&&"number"==typeof e.length){r&&(e=r);var n=0,i=function(){};return{s:i,n:function(){return n>=e.length?{done:!0}:{done:!1,value:e[n++]}},e:function(e){throw e},f:i}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var a,o=!0,l=!1;return{s:function(){r=e[Symbol.iterator]()},n:function(){var e=r.next();return o=e.done,e},e:function(e){l=!0,a=e},f:function(){try{o||null==r.return||r.return()}finally{if(l)throw a}}}}function s(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}var l=["climate","humidifier","water_heater"],c=["temperature","current_temperature","target_temp_low","target_temp_high","hvac_action","humidity","mode"],u=function(e,t,r,n){var i=arguments.length>4&&void 0!==arguments[4]&&arguments[4],a=arguments.length>5?arguments[5]:void 0,o=!(arguments.length>6&&void 0!==arguments[6])||arguments[6],s="history/period";return r&&(s+="/"+r.toISOString()),s+="?filter_entity_id="+t,n&&(s+="&end_time="+n.toISOString()),i&&(s+="&skip_initial_state"),void 0!==a&&(s+="&significant_changes_only=".concat(Number(a))),o&&(s+="&minimal_response"),e.callApi("GET",s)},d=function(e,t,r,n){return e.callApi("GET","history/period/".concat(t.toISOString(),"?end_time=").concat(r.toISOString(),"&minimal_response").concat(n?"&filter_entity_id=".concat(n):""))},f=function(e,t){return e.state===t.state&&(!e.attributes||!t.attributes||c.every((function(r){return e.attributes[r]===t.attributes[r]})))},h=function(e,t,r,s){var u={},d=[];return t?(t.forEach((function(t){if(0!==t.length){var l,c=t.find((function(e){return e.attributes&&"unit_of_measurement"in e.attributes}));c?l=c.attributes.unit_of_measurement:"climate"===(0,i.N)(t[0])||"water_heater"===(0,i.N)(t[0])?l=e.config.unit_system.temperature:"humidifier"===(0,i.N)(t[0])&&(l="%"),l?l in u?u[l].push(t):u[l]=[t]:d.push(function(e,t,r){var i,s=[],l=r.length-1,c=o(r);try{for(c.s();!(i=c.n()).done;){var u=i.value;s.length>0&&u.state===s[s.length-1].state||(u.entity_id||(u.attributes=r[l].attributes,u.entity_id=r[l].entity_id),s.push({state_localize:(0,n.D)(e,u,t),state:u.state,last_changed:u.last_changed}))}}catch(d){c.e(d)}finally{c.f()}return{name:(0,a.C)(r[0]),entity_id:r[0].entity_id,data:s}}(r,s,t))}})),{line:Object.keys(u).map((function(e){return function(e,t){var r,n=[],s=o(t);try{for(s.s();!(r=s.n()).done;){var u,d=r.value,h=d[d.length-1],p=(0,i.N)(h),y=[],m=o(d);try{for(m.s();!(u=m.n()).done;){var v=u.value,g=void 0;if(l.includes(p)){g={state:v.state,last_changed:v.last_updated,attributes:{}};var b,w=o(c);try{for(w.s();!(b=w.n()).done;){var k=b.value;k in v.attributes&&(g.attributes[k]=v.attributes[k])}}catch(_){w.e(_)}finally{w.f()}}else g=v;y.length>1&&f(g,y[y.length-1])&&f(g,y[y.length-2])||y.push(g)}}catch(_){m.e(_)}finally{m.f()}n.push({domain:p,name:(0,a.C)(h),entity_id:h.entity_id,states:y})}}catch(_){s.e(_)}finally{s.f()}return{unit:e,identifier:t.map((function(e){return e[0].entity_id})).join(""),data:n}}(e,u[e])})),timeline:d}):{line:[],timeline:[]}}},3542:function(e,t,r){"use strict";r.r(t);r(27849),r(53268),r(12730);var n=r(87744),i=(r(48932),r(92390),r(15652)),a=r(94707),o=r(11654),s=(r(44491),r(74535),r(58763));r(31206);function l(e){return(l="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function c(){var e=y(["\n        .content {\n          padding: 0 16px 16px;\n        }\n\n        .progress-wrapper {\n          height: calc(100vh - 136px);\n        }\n\n        :host([narrow]) .progress-wrapper {\n          height: calc(100vh - 198px);\n        }\n\n        .progress-wrapper {\n          position: relative;\n        }\n\n        ha-date-range-picker {\n          margin-right: 16px;\n          max-width: 100%;\n        }\n\n        :host([narrow]) ha-date-range-picker {\n          margin-right: 0;\n        }\n\n        ha-circular-progress {\n          position: absolute;\n          left: 50%;\n          top: 50%;\n          transform: translate(-50%, -50%);\n        }\n\n        ha-entity-picker {\n          display: inline-block;\n          flex-grow: 1;\n          max-width: 400px;\n        }\n\n        :host([narrow]) ha-entity-picker {\n          max-width: none;\n          width: 100%;\n        }\n      "]);return c=function(){return e},e}function u(e,t,r,n,i,a,o){try{var s=e[a](o),l=s.value}catch(c){return void r(c)}s.done?t(l):Promise.resolve(l).then(n,i)}function d(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function f(){var e=y(["\n                <state-history-charts\n                  .hass=","\n                  .historyData=","\n                  .endTime=","\n                  no-single\n                >\n                </state-history-charts>\n              "]);return f=function(){return e},e}function h(){var e=y(['<div class="progress-wrapper">\n                <ha-circular-progress\n                  active\n                  alt=',"\n                ></ha-circular-progress>\n              </div>"]);return h=function(){return e},e}function p(){var e=y(['\n      <ha-app-layout>\n        <app-header slot="header" fixed>\n          <app-toolbar>\n            <ha-menu-button\n              .hass=',"\n              .narrow=","\n            ></ha-menu-button>\n            <div main-title>",'</div>\n          </app-toolbar>\n        </app-header>\n\n        <div class="flex content">\n          <div class="flex layout horizontal wrap">\n            <ha-date-range-picker\n              .hass=',"\n              ?disabled=","\n              .startDate=","\n              .endDate=","\n              .ranges=","\n              @change=","\n            ></ha-date-range-picker>\n\n            <ha-entity-picker\n              .hass=","\n              .value=","\n              .label=","\n              .disabled=","\n              @change=","\n            ></ha-entity-picker>\n          </div>\n          ","\n        </div>\n      </ha-app-layout>\n    "]);return p=function(){return e},e}function y(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function m(e,t){return(m=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function v(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=C(e);if(t){var i=C(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return g(this,r)}}function g(e,t){return!t||"object"!==l(t)&&"function"!=typeof t?b(e):t}function b(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function w(){w=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var a="static"===i?e:r;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!D(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var a=this.decorateConstructor(r,t);return n.push.apply(n,a.finishers),a.finishers=n,a},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,a=i.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,i[a])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&n.push(l.finisher);var c=l.extras;if(c){for(var u=0;u<c.length;u++)this.addElementPlacement(c[u],t);r.push.apply(r,c)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==a.finisher&&r.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return O(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?O(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=P(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:S(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=S(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function k(e){var t,r=P(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function _(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function D(e){return e.decorators&&e.decorators.length}function E(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function S(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function P(e){var t=function(e,t){if("object"!==l(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==l(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===l(t)?t:String(t)}function O(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function x(e,t,r){return(x="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=C(e)););return e}(e,t);if(n){var i=Object.getOwnPropertyDescriptor(n,t);return i.get?i.get.call(r):i.value}})(e,t,r||e)}function C(e){return(C=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var j=function(e,t,r,n){var i=w();if(n)for(var a=0;a<n.length;a++)i=n[a](i);var o=t((function(e){i.initializeInstanceElements(e,s.elements)}),r),s=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},n=0;n<e.length;n++){var i,a=e[n];if("method"===a.kind&&(i=t.find(r)))if(E(a.descriptor)||E(i.descriptor)){if(D(a)||D(i))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");i.descriptor=a.descriptor}else{if(D(a)){if(D(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");i.decorators=a.decorators}_(a,i)}else t.push(a)}return t}(o.d.map(k)),e);return i.initializeClassElements(o.F,s.elements),i.runClassFinishers(o.F,s.finishers)}(null,(function(e,t){var r,l,y=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&m(e,t)}(n,t);var r=v(n);function n(){var t;!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,n),t=r.call(this),e(b(t));var i=new Date;i.setHours(i.getHours()-2),i.setMinutes(0),i.setSeconds(0),t._startDate=i;var a=new Date;return a.setHours(a.getHours()+1),a.setMinutes(0),a.setSeconds(0),t._endDate=a,t}return n}(t);return{F:y,d:[{kind:"field",decorators:[(0,i.Cb)()],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.Cb)({reflect:!0,type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"_startDate",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"_endDate",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"_entityId",value:function(){return""}},{kind:"field",decorators:[(0,i.Cb)()],key:"_isLoading",value:function(){return!1}},{kind:"field",decorators:[(0,i.Cb)()],key:"_stateHistory",value:void 0},{kind:"field",decorators:[(0,i.Cb)({reflect:!0,type:Boolean})],key:"rtl",value:function(){return!1}},{kind:"field",decorators:[(0,i.sz)()],key:"_ranges",value:void 0},{kind:"method",key:"render",value:function(){return(0,a.dy)(p(),this.hass,this.narrow,this.hass.localize("panel.history"),this.hass,this._isLoading,this._startDate,this._endDate,this._ranges,this._dateRangeChanged,this.hass,this._entityId,this.hass.localize("ui.components.entity.entity-picker.entity"),this._isLoading,this._entityPicked,this._isLoading?(0,a.dy)(h(),this.hass.localize("ui.common.loading")):(0,a.dy)(f(),this.hass,this._stateHistory,this._endDate))}},{kind:"method",key:"firstUpdated",value:function(e){var t;x(C(y.prototype),"firstUpdated",this).call(this,e);var r=new Date;r.setHours(0,0,0,0);var n=new Date(r);n.setDate(n.getDate()+1),n.setMilliseconds(n.getMilliseconds()-1);var i=new Date(r),a=new Date(i.setDate(r.getDate()-1)),o=new Date(a);o.setDate(o.getDate()+1),o.setMilliseconds(o.getMilliseconds()-1);var s=new Date(i.setDate(r.getDate()-r.getDay())),l=new Date(i.setDate(s.getDate()+7));l.setMilliseconds(l.getMilliseconds()-1);var c=new Date(i.setDate(r.getDate()-r.getDay()-7)),u=new Date(i.setDate(c.getDate()+7));u.setMilliseconds(u.getMilliseconds()-1),this._ranges=(d(t={},this.hass.localize("ui.panel.history.ranges.today"),[r,n]),d(t,this.hass.localize("ui.panel.history.ranges.yesterday"),[a,o]),d(t,this.hass.localize("ui.panel.history.ranges.this_week"),[s,l]),d(t,this.hass.localize("ui.panel.history.ranges.last_week"),[c,u]),t)}},{kind:"method",key:"updated",value:function(e){if((e.has("_startDate")||e.has("_endDate")||e.has("_entityId"))&&this._getHistory(),e.has("hass")){var t=e.get("hass");t&&t.language===this.hass.language||(this.rtl=(0,n.HE)(this.hass))}}},{kind:"method",key:"_getHistory",value:(r=regeneratorRuntime.mark((function e(){var t;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return this._isLoading=!0,e.next=3,(0,s._J)(this.hass,this._startDate,this._endDate,this._entityId);case 3:t=e.sent,this._stateHistory=(0,s.Nu)(this.hass,t,this.hass.localize,this.hass.language),this._isLoading=!1;case 6:case"end":return e.stop()}}),e,this)})),l=function(){var e=this,t=arguments;return new Promise((function(n,i){var a=r.apply(e,t);function o(e){u(a,n,i,o,s,"next",e)}function s(e){u(a,n,i,o,s,"throw",e)}o(void 0)}))},function(){return l.apply(this,arguments)})},{kind:"method",key:"_dateRangeChanged",value:function(e){this._startDate=e.detail.startDate;var t=e.detail.endDate;0===t.getHours()&&0===t.getMinutes()&&(t.setDate(t.getDate()+1),t.setMilliseconds(t.getMilliseconds()-1)),this._endDate=t}},{kind:"method",key:"_entityPicked",value:function(e){this._entityId=e.target.value}},{kind:"get",static:!0,key:"styles",value:function(){return[o.Qx,(0,i.iv)(c())]}}]}}),i.oi);customElements.define("ha-panel-history",j)}}]);
//# sourceMappingURL=chunk.22c9076354e6735468d7.js.map