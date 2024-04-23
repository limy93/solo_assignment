Feature: Make Payment

  As a logged-in customer
  I want to enter my payment details and submit payment
  So that I can complete my purchase

  Scenario: Successfully submit payment details
    Given I am logged in with valid credentials
    And I am on the Make Payment page
    When I fill in the payment form with valid details
    And I click the "Submit Payment" button
    Then I should be redirected to the Payment Status page
    And I should see a payment success message