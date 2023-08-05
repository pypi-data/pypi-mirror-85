(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[3979],{60280:(r,e,o)=>{"use strict";o.r(e),o.d(e,{HaImagecropperDialog:()=>b});o(53918);var t=o(82918),a=o.n(t),i=o(17692),n=o(15652),c=(o(34821),o(11654)),l=o(81471);function s(){s=function(){return r};var r={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(r,e){["method","field"].forEach((function(o){e.forEach((function(e){e.kind===o&&"own"===e.placement&&this.defineClassElement(r,e)}),this)}),this)},initializeClassElements:function(r,e){var o=r.prototype;["method","field"].forEach((function(t){e.forEach((function(e){var a=e.placement;if(e.kind===t&&("static"===a||"prototype"===a)){var i="static"===a?r:o;this.defineClassElement(i,e)}}),this)}),this)},defineClassElement:function(r,e){var o=e.descriptor;if("field"===e.kind){var t=e.initializer;o={enumerable:o.enumerable,writable:o.writable,configurable:o.configurable,value:void 0===t?void 0:t.call(r)}}Object.defineProperty(r,e.key,o)},decorateClass:function(r,e){var o=[],t=[],a={static:[],prototype:[],own:[]};if(r.forEach((function(r){this.addElementPlacement(r,a)}),this),r.forEach((function(r){if(!m(r))return o.push(r);var e=this.decorateElement(r,a);o.push(e.element),o.push.apply(o,e.extras),t.push.apply(t,e.finishers)}),this),!e)return{elements:o,finishers:t};var i=this.decorateConstructor(o,e);return t.push.apply(t,i.finishers),i.finishers=t,i},addElementPlacement:function(r,e,o){var t=e[r.placement];if(!o&&-1!==t.indexOf(r.key))throw new TypeError("Duplicated element ("+r.key+")");t.push(r.key)},decorateElement:function(r,e){for(var o=[],t=[],a=r.decorators,i=a.length-1;i>=0;i--){var n=e[r.placement];n.splice(n.indexOf(r.key),1);var c=this.fromElementDescriptor(r),l=this.toElementFinisherExtras((0,a[i])(c)||c);r=l.element,this.addElementPlacement(r,e),l.finisher&&t.push(l.finisher);var s=l.extras;if(s){for(var d=0;d<s.length;d++)this.addElementPlacement(s[d],e);o.push.apply(o,s)}}return{element:r,finishers:t,extras:o}},decorateConstructor:function(r,e){for(var o=[],t=e.length-1;t>=0;t--){var a=this.fromClassDescriptor(r),i=this.toClassDescriptor((0,e[t])(a)||a);if(void 0!==i.finisher&&o.push(i.finisher),void 0!==i.elements){r=i.elements;for(var n=0;n<r.length-1;n++)for(var c=n+1;c<r.length;c++)if(r[n].key===r[c].key&&r[n].placement===r[c].placement)throw new TypeError("Duplicated element ("+r[n].key+")")}}return{elements:r,finishers:o}},fromElementDescriptor:function(r){var e={kind:r.kind,key:r.key,placement:r.placement,descriptor:r.descriptor};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===r.kind&&(e.initializer=r.initializer),e},toElementDescriptors:function(r){var e;if(void 0!==r)return(e=r,function(r){if(Array.isArray(r))return r}(e)||function(r){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(r))return Array.from(r)}(e)||function(r,e){if(r){if("string"==typeof r)return v(r,e);var o=Object.prototype.toString.call(r).slice(8,-1);return"Object"===o&&r.constructor&&(o=r.constructor.name),"Map"===o||"Set"===o?Array.from(r):"Arguments"===o||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(o)?v(r,e):void 0}}(e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(r){var e=this.toElementDescriptor(r);return this.disallowProperty(r,"finisher","An element descriptor"),this.disallowProperty(r,"extras","An element descriptor"),e}),this)},toElementDescriptor:function(r){var e=String(r.kind);if("method"!==e&&"field"!==e)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+e+'"');var o=u(r.key),t=String(r.placement);if("static"!==t&&"prototype"!==t&&"own"!==t)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+t+'"');var a=r.descriptor;this.disallowProperty(r,"elements","An element descriptor");var i={kind:e,key:o,placement:t,descriptor:Object.assign({},a)};return"field"!==e?this.disallowProperty(r,"initializer","A method descriptor"):(this.disallowProperty(a,"get","The property descriptor of a field descriptor"),this.disallowProperty(a,"set","The property descriptor of a field descriptor"),this.disallowProperty(a,"value","The property descriptor of a field descriptor"),i.initializer=r.initializer),i},toElementFinisherExtras:function(r){return{element:this.toElementDescriptor(r),finisher:f(r,"finisher"),extras:this.toElementDescriptors(r.extras)}},fromClassDescriptor:function(r){var e={kind:"class",elements:r.map(this.fromElementDescriptor,this)};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),e},toClassDescriptor:function(r){var e=String(r.kind);if("class"!==e)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+e+'"');this.disallowProperty(r,"key","A class descriptor"),this.disallowProperty(r,"placement","A class descriptor"),this.disallowProperty(r,"descriptor","A class descriptor"),this.disallowProperty(r,"initializer","A class descriptor"),this.disallowProperty(r,"extras","A class descriptor");var o=f(r,"finisher");return{elements:this.toElementDescriptors(r.elements),finisher:o}},runClassFinishers:function(r,e){for(var o=0;o<e.length;o++){var t=(0,e[o])(r);if(void 0!==t){if("function"!=typeof t)throw new TypeError("Finishers must return a constructor.");r=t}}return r},disallowProperty:function(r,e,o){if(void 0!==r[e])throw new TypeError(o+" can't have a ."+e+" property.")}};return r}function d(r){var e,o=u(r.key);"method"===r.kind?e={value:r.value,writable:!0,configurable:!0,enumerable:!1}:"get"===r.kind?e={get:r.value,configurable:!0,enumerable:!1}:"set"===r.kind?e={set:r.value,configurable:!0,enumerable:!1}:"field"===r.kind&&(e={configurable:!0,writable:!0,enumerable:!0});var t={kind:"field"===r.kind?"field":"method",key:o,placement:r.static?"static":"field"===r.kind?"own":"prototype",descriptor:e};return r.decorators&&(t.decorators=r.decorators),"field"===r.kind&&(t.initializer=r.value),t}function p(r,e){void 0!==r.descriptor.get?e.descriptor.get=r.descriptor.get:e.descriptor.set=r.descriptor.set}function m(r){return r.decorators&&r.decorators.length}function h(r){return void 0!==r&&!(void 0===r.value&&void 0===r.writable)}function f(r,e){var o=r[e];if(void 0!==o&&"function"!=typeof o)throw new TypeError("Expected '"+e+"' to be a function");return o}function u(r){var e=function(r,e){if("object"!=typeof r||null===r)return r;var o=r[Symbol.toPrimitive];if(void 0!==o){var t=o.call(r,e||"default");if("object"!=typeof t)return t;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===e?String:Number)(r)}(r,"string");return"symbol"==typeof e?e:String(e)}function v(r,e){(null==e||e>r.length)&&(e=r.length);for(var o=0,t=new Array(e);o<e;o++)t[o]=r[o];return t}let b=function(r,e,o,t){var a=s();if(t)for(var i=0;i<t.length;i++)a=t[i](a);var n=e((function(r){a.initializeInstanceElements(r,c.elements)}),o),c=a.decorateClass(function(r){for(var e=[],o=function(r){return"method"===r.kind&&r.key===i.key&&r.placement===i.placement},t=0;t<r.length;t++){var a,i=r[t];if("method"===i.kind&&(a=e.find(o)))if(h(i.descriptor)||h(a.descriptor)){if(m(i)||m(a))throw new ReferenceError("Duplicated methods ("+i.key+") can't be decorated.");a.descriptor=i.descriptor}else{if(m(i)){if(m(a))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+i.key+").");a.decorators=i.decorators}p(i,a)}else e.push(i)}return e}(n.d.map(d)),r);return a.initializeClassElements(n.F,c.elements),a.runClassFinishers(n.F,c.finishers)}([(0,n.Mo)("image-cropper-dialog")],(function(r,e){return{F:class extends e{constructor(...e){super(...e),r(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,n.sz)()],key:"_open",value:()=>!1},{kind:"field",decorators:[(0,n.IO)("img",!0)],key:"_image",value:void 0},{kind:"field",key:"_cropper",value:void 0},{kind:"method",key:"showDialog",value:function(r){this._params=r,this._open=!0}},{kind:"method",key:"closeDialog",value:function(){var r;this._open=!1,this._params=void 0,null===(r=this._cropper)||void 0===r||r.destroy()}},{kind:"method",key:"updated",value:function(r){r.has("_params")&&this._params&&(this._cropper?this._cropper.replace(URL.createObjectURL(this._params.file)):(this._image.src=URL.createObjectURL(this._params.file),this._cropper=new(a())(this._image,{aspectRatio:this._params.options.aspectRatio,viewMode:1,dragMode:"move",minCropBoxWidth:50,ready:()=>{URL.revokeObjectURL(this._image.src)}})))}},{kind:"method",key:"render",value:function(){var r;return n.dy`<ha-dialog
      @closed=${this.closeDialog}
      scrimClickAction
      escapeKeyAction
      .open=${this._open}
    >
      <div
        class="container ${(0,l.$)({round:Boolean(null===(r=this._params)||void 0===r?void 0:r.options.round)})}"
      >
        <img />
      </div>
      <mwc-button slot="secondaryAction" @click=${this.closeDialog}>
        ${this.hass.localize("ui.common.cancel")}
      </mwc-button>
      <mwc-button slot="primaryAction" @click=${this._cropImage}>
        ${this.hass.localize("ui.dialogs.image_cropper.crop")}
      </mwc-button>
    </ha-dialog>`}},{kind:"method",key:"_cropImage",value:function(){this._cropper.getCroppedCanvas().toBlob((r=>{if(!r)return;const e=new File([r],this._params.file.name,{type:this._params.options.type||this._params.file.type});this._params.croppedCallback(e),this.closeDialog()}),this._params.options.type||this._params.file.type,this._params.options.quality)}},{kind:"get",static:!0,key:"styles",value:function(){return[c.yu,n.iv`
        ${(0,n.$m)(i.Z)}
        .container {
          max-width: 640px;
        }
        img {
          max-width: 100%;
        }
        .container.round .cropper-view-box,
        .container.round .cropper-face {
          border-radius: 50%;
        }
        .cropper-line,
        .cropper-point,
        .cropper-point.point-se::before {
          background-color: var(--primary-color);
        }
      `]}}]}}),n.oi)},11654:(r,e,o)=>{"use strict";o.d(e,{_l:()=>a,q0:()=>i,Qx:()=>n,yu:()=>c,$c:()=>l});var t=o(15652);const a={"primary-background-color":"#111111","card-background-color":"#1c1c1c","secondary-background-color":"#202020","primary-text-color":"#e1e1e1","secondary-text-color":"#9b9b9b","disabled-text-color":"#6f6f6f","app-header-text-color":"#e1e1e1","app-header-background-color":"#1c1c1c","switch-unchecked-button-color":"#999999","switch-unchecked-track-color":"#9b9b9b","divider-color":"rgba(225, 225, 225, .12)","mdc-ripple-color":"#AAAAAA","codemirror-keyword":"#C792EA","codemirror-operator":"#89DDFF","codemirror-variable":"#f07178","codemirror-variable-2":"#EEFFFF","codemirror-variable-3":"#DECB6B","codemirror-builtin":"#FFCB6B","codemirror-atom":"#F78C6C","codemirror-number":"#FF5370","codemirror-def":"#82AAFF","codemirror-string":"#C3E88D","codemirror-string-2":"#f07178","codemirror-comment":"#545454","codemirror-tag":"#FF5370","codemirror-meta":"#FFCB6B","codemirror-attribute":"#C792EA","codemirror-property":"#C792EA","codemirror-qualifier":"#DECB6B","codemirror-type":"#DECB6B"},i={"error-state-color":"var(--error-color)","state-icon-unavailable-color":"var(--disabled-text-color)","sidebar-text-color":"var(--primary-text-color)","sidebar-background-color":"var(--card-background-color)","sidebar-selected-text-color":"var(--primary-color)","sidebar-selected-icon-color":"var(--primary-color)","sidebar-icon-color":"rgba(var(--rgb-primary-text-color), 0.6)","switch-checked-color":"var(--primary-color)","switch-checked-button-color":"var(--switch-checked-color, var(--primary-background-color))","switch-checked-track-color":"var(--switch-checked-color, #000000)","switch-unchecked-button-color":"var(--switch-unchecked-color, var(--primary-background-color))","switch-unchecked-track-color":"var(--switch-unchecked-color, #000000)","slider-color":"var(--primary-color)","slider-secondary-color":"var(--light-primary-color)","slider-bar-color":"var(--disabled-text-color)","label-badge-grey":"var(--paper-grey-500)","label-badge-background-color":"var(--card-background-color)","label-badge-text-color":"rgba(var(--rgb-primary-text-color), 0.8)","paper-listbox-background-color":"var(--card-background-color)","paper-item-icon-color":"var(--state-icon-color)","paper-item-icon-active-color":"var(--state-icon-active-color)","table-row-background-color":"var(--primary-background-color)","table-row-alternative-background-color":"var(--secondary-background-color)","paper-slider-knob-color":"var(--slider-color)","paper-slider-knob-start-color":"var(--slider-color)","paper-slider-pin-color":"var(--slider-color)","paper-slider-pin-start-color":"var(--slider-color)","paper-slider-active-color":"var(--slider-color)","paper-slider-secondary-color":"var(--slider-secondary-color)","paper-slider-container-color":"var(--slider-bar-color)","data-table-background-color":"var(--card-background-color)","markdown-code-background-color":"var(--primary-background-color)","mdc-theme-primary":"var(--primary-color)","mdc-theme-secondary":"var(--accent-color)","mdc-theme-background":"var(--primary-background-color)","mdc-theme-surface":"var(--card-background-color)","mdc-theme-on-primary":"var(--text-primary-color)","mdc-theme-on-secondary":"var(--text-primary-color)","mdc-theme-on-surface":"var(--primary-text-color)","mdc-theme-text-primary-on-background":"var(--primary-text-color)","mdc-theme-text-secondary-on-background":"var(--secondary-text-color)","mdc-theme-text-icon-on-background":"var(--secondary-text-color)","app-header-text-color":"var(--text-primary-color)","app-header-background-color":"var(--primary-color)","material-body-text-color":"var(--primary-text-color)","material-background-color":"var(--card-background-color)","material-secondary-background-color":"var(--secondary-background-color)","material-secondary-text-color":"var(--secondary-text-color)","mdc-checkbox-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-checkbox-disabled-color":"var(--disabled-text-color)","mdc-radio-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-radio-disabled-color":"var(--disabled-text-color)","mdc-tab-text-label-color-default":"var(--primary-text-color)","mdc-button-disabled-ink-color":"var(--disabled-text-color)","mdc-button-outline-color":"var(--divider-color)","mdc-dialog-scroll-divider-color":"var(--divider-color)"},n=t.iv`
  :host {
    font-family: var(--paper-font-body1_-_font-family);
    -webkit-font-smoothing: var(--paper-font-body1_-_-webkit-font-smoothing);
    font-size: var(--paper-font-body1_-_font-size);
    font-weight: var(--paper-font-body1_-_font-weight);
    line-height: var(--paper-font-body1_-_line-height);
  }

  app-header-layout,
  ha-app-layout {
    background-color: var(--primary-background-color);
  }

  app-header,
  app-toolbar {
    background-color: var(--app-header-background-color);
    font-weight: 400;
    color: var(--app-header-text-color, white);
  }

  app-toolbar {
    height: var(--header-height);
  }

  app-header div[sticky] {
    height: 48px;
  }

  app-toolbar [main-title] {
    margin-left: 20px;
  }

  h1 {
    font-family: var(--paper-font-headline_-_font-family);
    -webkit-font-smoothing: var(--paper-font-headline_-_-webkit-font-smoothing);
    white-space: var(--paper-font-headline_-_white-space);
    overflow: var(--paper-font-headline_-_overflow);
    text-overflow: var(--paper-font-headline_-_text-overflow);
    font-size: var(--paper-font-headline_-_font-size);
    font-weight: var(--paper-font-headline_-_font-weight);
    line-height: var(--paper-font-headline_-_line-height);
  }

  h2 {
    font-family: var(--paper-font-title_-_font-family);
    -webkit-font-smoothing: var(--paper-font-title_-_-webkit-font-smoothing);
    white-space: var(--paper-font-title_-_white-space);
    overflow: var(--paper-font-title_-_overflow);
    text-overflow: var(--paper-font-title_-_text-overflow);
    font-size: var(--paper-font-title_-_font-size);
    font-weight: var(--paper-font-title_-_font-weight);
    line-height: var(--paper-font-title_-_line-height);
  }

  h3 {
    font-family: var(--paper-font-subhead_-_font-family);
    -webkit-font-smoothing: var(--paper-font-subhead_-_-webkit-font-smoothing);
    white-space: var(--paper-font-subhead_-_white-space);
    overflow: var(--paper-font-subhead_-_overflow);
    text-overflow: var(--paper-font-subhead_-_text-overflow);
    font-size: var(--paper-font-subhead_-_font-size);
    font-weight: var(--paper-font-subhead_-_font-weight);
    line-height: var(--paper-font-subhead_-_line-height);
  }

  a {
    color: var(--primary-color);
  }

  .secondary {
    color: var(--secondary-text-color);
  }

  .error {
    color: var(--error-color);
  }

  .warning {
    color: var(--error-color);
  }

  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }

  button.link {
    background: none;
    color: inherit;
    border: none;
    padding: 0;
    font: inherit;
    text-align: left;
    text-decoration: underline;
    cursor: pointer;
  }

  .card-actions a {
    text-decoration: none;
  }

  .card-actions .warning {
    --mdc-theme-primary: var(--error-color);
  }

  .layout.horizontal,
  .layout.vertical {
    display: flex;
  }
  .layout.inline {
    display: inline-flex;
  }
  .layout.horizontal {
    flex-direction: row;
  }
  .layout.vertical {
    flex-direction: column;
  }
  .layout.wrap {
    flex-wrap: wrap;
  }
  .layout.no-wrap {
    flex-wrap: nowrap;
  }
  .layout.center,
  .layout.center-center {
    align-items: center;
  }
  .layout.bottom {
    align-items: flex-end;
  }
  .layout.center-justified,
  .layout.center-center {
    justify-content: center;
  }
  .flex {
    flex: 1;
    flex-basis: 0.000000001px;
  }
  .flex-auto {
    flex: 1 1 auto;
  }
  .flex-none {
    flex: none;
  }
  .layout.justified {
    justify-content: space-between;
  }
`,c=t.iv`
  /* prevent clipping of positioned elements */
  paper-dialog-scrollable {
    --paper-dialog-scrollable: {
      -webkit-overflow-scrolling: auto;
    }
  }

  /* force smooth scrolling for iOS 10 */
  paper-dialog-scrollable.can-scroll {
    --paper-dialog-scrollable: {
      -webkit-overflow-scrolling: touch;
    }
  }

  .paper-dialog-buttons {
    align-items: flex-end;
    padding: 8px;
    padding-bottom: max(env(safe-area-inset-bottom), 8px);
  }

  @media all and (min-width: 450px) and (min-height: 500px) {
    ha-paper-dialog {
      min-width: 400px;
    }
  }

  @media all and (max-width: 450px), all and (max-height: 500px) {
    paper-dialog,
    ha-paper-dialog {
      margin: 0;
      width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      min-width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      max-width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      max-height: calc(100% - var(--header-height));

      position: fixed !important;
      bottom: 0px;
      left: env(safe-area-inset-left);
      right: env(safe-area-inset-right);
      overflow: scroll;
      border-bottom-left-radius: 0px;
      border-bottom-right-radius: 0px;
    }
  }

  /* mwc-dialog (ha-dialog) styles */
  ha-dialog {
    --mdc-dialog-min-width: 400px;
    --mdc-dialog-max-width: 600px;
    --mdc-dialog-heading-ink-color: var(--primary-text-color);
    --mdc-dialog-content-ink-color: var(--primary-text-color);
    --justify-action-buttons: space-between;
  }

  ha-dialog .form {
    padding-bottom: 24px;
    color: var(--primary-text-color);
  }

  a {
    color: var(--primary-color);
  }

  /* make dialog fullscreen on small screens */
  @media all and (max-width: 450px), all and (max-height: 500px) {
    ha-dialog {
      --mdc-dialog-min-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-max-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-min-height: 100%;
      --mdc-dialog-max-height: 100%;
      --mdc-shape-medium: 0px;
      --vertial-align-dialog: flex-end;
    }
  }
  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }
  .error {
    color: var(--error-color);
  }
`,l=t.iv`
  .ha-scrollbar::-webkit-scrollbar {
    width: 0.4rem;
    height: 0.4rem;
  }

  .ha-scrollbar::-webkit-scrollbar-thumb {
    -webkit-border-radius: 4px;
    border-radius: 4px;
    background: var(--scrollbar-thumb-color);
  }

  .ha-scrollbar {
    overflow-y: auto;
    scrollbar-color: var(--scrollbar-thumb-color) transparent;
    scrollbar-width: thin;
  }
`}}]);
//# sourceMappingURL=chunk.d1faedad4b55ad239944.js.map