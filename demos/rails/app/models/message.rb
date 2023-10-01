class Message < ApplicationRecord
  validates :body, presence: true
end
