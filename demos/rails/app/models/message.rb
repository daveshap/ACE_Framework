# frozen_string_literal: true

class Message < ApplicationRecord
  validates :body, presence: true
end
