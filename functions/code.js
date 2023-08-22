import { getZip_Uid } from './utils'

// This function is the one Netlify function runs on
// https://docs.netlify.com/functions/build-with-javascript/#synchronous-function-format
exports.handler = async function (event, _) {
  // event is a JSON object
  const data = JSON.parse(event.body)
  const { zipRes, nbUid } = await getZip_Uid(data)

  return {
    statusCode: 200,
    body: zipRes
  }
}
