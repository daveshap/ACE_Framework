class SendMessageJob < ApplicationJob
  queue_as :default

  def perform(message)
    client = OpenAI::Client.new
    response = client.chat(
      parameters: {
        model: "gpt-3.5-turbo",
        messages: [{ role: "user", content: message.body}],
        temperature: 0.7
      }
    )
    pp response
    puts response.dig("choices", 0, "message", "content")
  end
end
