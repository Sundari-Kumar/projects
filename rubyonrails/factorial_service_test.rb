require 'test_helper'

class FactorialServiceTest < ActiveSupport::TestCase
  def setup
    @service = FactorialService.new
  end

  test "returns 1 for factorial of 0" do
    assert_equal 1, @service.calculate(0)
  end

  test "returns 1 for factorial of 1" do
    assert_equal 1, @service.calculate(1)
  end

  test "returns 120 for factorial of 5" do
    assert_equal 120, @service.calculate(5)
  end

  test "raises error for negative number" do
    assert_raises(ArgumentError) { @service.calculate(-1) }
  end
end
