Feature: Make Payment
  As a logged-in customer
  I want to enter my payment details and submit payment
  So that I can complete my purchase

Background:
  Given I have already registered
  and I have logged in to my account
  And products are added to my cart

  Scenario: Successfully submit payment details
    Given I am on the Make Payment page
    When I fill in the payment form with valid details
    And I click the "Submit Payment" button
    Then I should be redirected to the Payment Status page
    And I should see a payment success message