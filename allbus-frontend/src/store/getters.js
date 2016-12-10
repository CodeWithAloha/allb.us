function natCmp (a, b) {
  var ra = a.match(/\D+|\d+/g)
  var rb = b.match(/\D+|\d+/g)
  var r = 0

  while (!r && ra.length && rb.length) {
    var x = ra.shift()
    var y = rb.shift()
    var nx = parseInt(x)
    var ny = parseInt(y)

    if (isNaN(nx) || isNaN(ny)) {
      r = x > y ? 1 : (x < y ? -1 : 0)
    } else {
      r = nx - ny
    }
  }
  return r || ra.length - rb.length
}

export function sortedRouteNames (state) {
  return state.stop.route_names.sort(natCmp)
}
